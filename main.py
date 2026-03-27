import streamlit as st
from scrape import scrape_website, split_dom_content, clean_body_content, extract_body_content
from parse import parse_with_ollama
import json
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed

st.title("AI Web Scraper")
urls_input = st.text_area('Enter URLs (one per line):')
urls = [u.strip() for u in urls_input.split("\n") if u.strip()]

if st.button('Scrape'):
    st.write('Scraping the website')

    all_clean_content = []

    # for url in urls:
    #     st.write(f"Scraping: {url}")
    #     result = scrape_website(url)

    #     if result:
    #         body_content = extract_body_content(result)
    #         clean_content = clean_body_content(body_content)
    #         all_clean_content.append(f"URL: {url}\n{clean_content}")
    def process_url(url):
        try:
            result = scrape_website(url)
            if result:
                body_content = extract_body_content(result)
                clean_content = clean_body_content(body_content)
                return f"URL: {url}\n{clean_content}"
        except Exception as e:
            return f"URL: {url}\nERROR: {e}"
        
        return None
    
    progress = st.progress(0)
    status = st.empty()

    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {executor.submit(process_url, url): url for url in urls}

        for i, future in enumerate(as_completed(futures)):
            url = futures[future]
            result = future.result()

            if result:
                all_clean_content.append(result)

            progress.progress((i + 1) / len(urls))
            status.write(f"Completed: {url}")

    combined_content = "\n".join(all_clean_content)

    st.session_state.dom_content = all_clean_content

    with st.expander('View DOM Contents'):
        st.text_area('DOM Contents', "\n\n".join(all_clean_content), height=300)

if 'dom_content' in st.session_state:
    parse_description = st.text_area('Describe what you want to parse?')

    if st.button('Parse Contents'):
        if parse_description:

            # dom_chunks = split_dom_content(st.session_state.dom_content)
            # with st.spinner("Parsing content with AI.."):
            #     result = parse_with_ollama(dom_chunks, parse_description)
            # st.success("Parsing completed successfully")

            all_results = []

            for content in st.session_state.dom_content:
                dom_chunks = split_dom_content(content)

                with st.spinner("Parsing content with AI..."):
                    result = parse_with_ollama(dom_chunks, parse_description)

                try:
                    parsed = json.loads(result)
                    
                    if isinstance(parsed, list):
                        all_results.extend(parsed)
                    else:
                        all_results.append(parsed)

                except:
                    continue
            
            parsed_json = all_results

            try:
                # parsed_json = json.loads(result)

                if isinstance(parsed_json, list):
                    st.write(f"Extracted {len(parsed_json)} records")
                    
                st.subheader('Parsed Output')
                st.json(parsed_json, expanded=True)
                st.code(json.dumps(parsed_json, indent=2), language="json")

                st.download_button(
                    label="Download JSON",
                    data=json.dumps(parsed_json, indent=2),
                    file_name="parsed_data.json",
                    mime="application/json"
                )

                if isinstance(parsed_json, list):
                    df = pd.json_normalize(parsed_json)
                    st.download_button(
                        label="Download CSV",
                        data=df.to_csv(index=False),
                        file_name="parsed_data.csv",
                        mime="text/csv"                       
                    )

            except:
                st.write(result)