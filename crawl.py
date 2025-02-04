import requests
import xml.etree.ElementTree as ET

def get_sitemap_links(sitemap_url, filter_path="/doc/"):
    """解析 `sitemap.xml` 并返回符合筛选条件的网页链接"""
    try:
        response = requests.get(sitemap_url, timeout=10)
        if response.status_code != 200:
            print(f"⚠️ Failed to fetch sitemap: {sitemap_url}")
            return []

        sitemap_xml = response.text
        root = ET.fromstring(sitemap_xml)
        namespaces = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}

        # 获取所有链接
        urls = [elem.text for elem in root.findall(".//ns:loc", namespaces)]
        
        # 只保留符合 `filter_path` 的链接
        filtered_urls = [url for url in urls if filter_path in url]
        
        return filtered_urls
    except Exception as e:
        print(f"⚠️ Error parsing sitemap {sitemap_url}: {e}")
        return []

if __name__ == "__main__":
    sitemap_url = "https://python.langchain.com/sitemap.xml"
    filtered_pages = get_sitemap_links(sitemap_url, filter_path="https://python.langchain.com/docs/integrations/chat/")

    # 🔢 统计数量
    print(f"\n🔗 Found {len(filtered_pages)} Pages in Sitemap:")
    # for url in sorted(filtered_pages):
    #     print(url)