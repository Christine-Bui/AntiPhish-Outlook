import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import re
import tldextract
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
from collections import Counter
import ipaddress
from sklearn.ensemble import RandomForestClassifier
import statistics as stats

def preprocess_email_content(email_content):
    print("Preprocessing email contents...")
    extracted = email_content['email_contents']
    preprocessed_content = extracted.lower()
    return preprocessed_content

def transform_email_to_features(preprocessed_email_content):
    # Initialize a list to store the extracted features
    email_features = []
    multiple_links = []

    #check if there are links
    # has_link = re.findall(r'\<.*?\>', preprocess_email_content)
    url_pattern = re.compile(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+')
    has_link = url_pattern.findall(preprocessed_email_content)
    # GET request to URL
    response = requests.get(has_link)
    # pasrse HTML content
    temp = BeautifulSoup(response.content, 'html.parser')
    html_content = response.text
    #if there are links, get data to check if phishing (im assuming theres one link for now)
    if len(has_link) != 0:
        for i in range(0, len(has_link)):
            #expecting multiple links in the email
            if len(email_features) != 0:
                multiple_links.append(email_features)
            email_features.clear()
            # Extract ID
            email_features.append(re.findall('\d+',has_link[i]))
            # Extract NumDots from preprocessed_email_content
            num_dots = has_link[i].count(".")
            email_features.append(num_dots) 
            # Extract SubdomainLevel
            ext = tldextract.extract(has_link[i]) #https://pypi.org/project/tldextract/
            sub = ext.subdomain
            sub.split('.')
            email_features.append(sub.size)
            # Extract PathLevel
            path = urlparse.urlparse(has_link[i])
            path.split('/')
            email_features.append(len(path))
            # Extract UrlLength
            email_features.append(len(has_link[i]))
            # Extract NumDash from preprocessed_email_content
            num_dash = has_link[i].count("-")
            email_features.append(num_dash)
            # Extract NumDashInHostname
            ext = tldextract.extract(has_link[i])
            domain = ext.domain
            num_dash_in_domain = domain.count("-")
            email_features.append(num_dash_in_domain)
            # Extract AtSymbol
            if "@" in has_link[i]:
                print("At symbol found in URL")
                result = 1
            else:
                print("At symbol not found in URL")
                result = 0
            email_features.append(result)
            # Extract TildeSymbol
            if "~" in has_link[i]:
                print("At symbol found in URL")
                result = 1
            else:
                print("At symbol not found in URL")
                result = 0
            email_features.append(result)
            # Extract NumUnderscore from preprocessed_email_content
            num_underscore = has_link[i].count("_")
            email_features.append(num_underscore)
            # Extract NumPercent from preprocessed_email_content
            num_percent = has_link[i].count("%")
            email_features.append(num_percent)
            #Extract NumQueryComponents
            num_query_components = has_link[i].count("?")
            email_features.append(num_query_components)
            # Extract NumAmpersand from preprocessed_email_content
            num_ampersand = has_link[i].count("&")
            email_features.append(num_ampersand)
            # Extract NumHash from preprocessed_email_content
            num_hash = has_link[i].count("#")
            email_features.append(num_hash)
            # Extract NumNumericChars from preprocessed_email_content
            num_numeric_chars = sum(c.isdigit() for c in has_link[i])
            email_features.append(num_numeric_chars)
            # Extract NoHttps
            pattern = r"^https"
            match = re.search(pattern, has_link[i])
            if match:
                print("At symbol found in URL")
                result = 1
            else:
                print("At symbol not found in URL")
                result = 0
            email_features.append(result)
            # Extract RandomString
            pattern = r"[a-z0-9]{8,}"
            matches = re.findall(pattern, has_link[i])
            if matches:
                result = 1
                print("Random string found")
            else:
                result = 0
                print("Random string not found")
            email_features.append(result)
            # Extract IpAddress
            header = preprocess_email_content.get('Received')
            ip_address = re.search(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', header).group(0)
            url = "https://" + ip_address + "/page.html"
            parsed_url = url.parse.urlparse(url)
            hostname = parsed_url.hostname
            try:
                ipaddress.ip_address(hostname)
                print("The hostname is an IP address.")
                result = 1
            except ValueError:
                print("The hostname is not an IP address.")
                result = 0
            email_features.append(result)
            # Extract DomainInSubdomains
            subdomain, _, tld = tldextract.extract(has_link[i])
            if tld in subdomain:
                print("The TLD or ccTLD is used in the subdomain.")
                result = 1
            else:
                print("The TLD or ccTLD is not used in the subdomain.")
                result = 0
            email_features.append(result)
            # Extract DomainInPaths
            path = urlparse.urlparse(has_link[i])
            tld = tldextract.extract(path).suffix
            if tld:
                print("The TLD or ccTLD is used in the path.")
                result = 1
            else:
                print("The TLD or ccTLD is not used in the path.")
                result = 0
            email_features.append(result)
            # Extract HttpsInHostname
            parsed_url = urlparse.unquote(has_link[i])
            hostname = urlparse.urlparse(parsed_url).hostname
            if re.search(r"https", hostname):
                print("HTTPS is obfuscated in the hostname.")
                result = 1
            else:
                print("HTTPS is not obfuscated in the hostname.")
                result = 0
            email_features.append(result)
            # Extract HostnameLength
            ext = tldextract.extract(has_link[i])
            domain = ext.domain
            email_features.append(len(domain))
            # Extract PathLength
            path = urlparse.urlparse(has_link[i])
            email_features.append(len(path))
            # Extract QueryLength
            queries = has_link.split("?")
            query_length = 0
            for i in queries[1:]:
                query_length = query_length + len(queries[i])
            email_features.append(query_length)
            # Extract DoubleSlashInPath
            parsed_url = urlparse.urlparse(has_link[i])
            path = parsed_url.path
            if re.search(r"\/\/", path):
                print("// exists in the path.")
                result = 1
            else:
                print("// does not exist in the path.")
                result = 0
            email_features.append(result)
            # Extract NumSensitiveWords
            sensitive_words = ["secure", "account", "webscr", "login", "ebayisapi", "signin", "banking", "confirm"]
            num_sensitive_words = sum([1 for word in sensitive_words if re.search(word, has_link[i], re.IGNORECASE)])
            email_features.append(num_sensitive_words)
            # Extract EmbeddedBrandName
            domain_names = [urlparse(link.get("href")).hostname for link in temp.find_all("a") if link.get("href")]
            domain_name_counts = Counter(domain_names)
            most_frequent_domain_name = domain_name_counts.most_common(1)[0][0]
            parsed_url = urlparse(has_link[i])
            subdomains = parsed_url.hostname.split(".")[:-2]
            path = parsed_url.path
            if most_frequent_domain_name in subdomains or most_frequent_domain_name in path:
                result = 1
                print("Brand name embedded")
            else:
                result = 0
                print("Brand name not embedded")
            email_features.append(result)
            # Extract PctExtHyperlinks (Counts the percentage of external hyperlinks in webpage HTML source code)
            #TODO: line 216, in findall
            #return _compile(pattern, flags).findall(string)
            #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            #TypeError: expected string or bytes-like object, got 'function'
            if has_link:
                for link in has_link:
                    response = requests.get(link.decode())
                    total_links = 0
                    external_links = 0
                    for link in temp.find_all('a'):
                        href = link.get('href')
                        if href and (href.startswith('http') or href.startswith('//')):
                            domain = tldextract.extract(href).domain
                            if domain != tldextract.extract(link).domain:
                                external_links += 1
                            total_links += 1
                    if total_links > 0:
                        pct_external_links = (external_links / total_links) * 100
                        print(f"Percentage of external hyperlinks: {pct_external_links:.2f}")
                        result = format(pct_external_links, '.2f')[1:]
                    else:
                        print("No hyperlinks found in HTML")
                        result = 0
                    email_features.append(result)
            # Extract PctExtResourceUrls
            total_resources = 0
            external_resources = 0
            for tag in temp.find_all():
                if tag.has_attr('href'):
                    href = tag['href']
                    if href.startswith('http') or href.startswith('//'):
                        domain = tldextract.extract(href).domain
                        if domain != tldextract.extract(has_link[i]).domain:
                            external_resources += 1
                    total_resources += 1
                if tag.has_attr('src'):
                    src = tag['src']
                    if src.startswith('http') or src.startswith('//'):
                        domain = tldextract.extract(src).domain
                        if domain != tldextract.extract(has_link[i]).domain:
                            external_resources += 1
                    total_resources += 1
            if total_resources > 0:
                pct_external_resources = (external_resources / total_resources) * 100
                print(f"Percentage of external resource URLs: {pct_external_resources:.2f}%")
                result = format(pct_external_resources, '.2f')[1:]
            else:
                print("No resource URLs found in HTML")
                result = 0
            email_features.append(result)
            # Extract ExtFavicon
            for link in temp.find_all('link', rel='icon'):
                href = link.get('href')
                if href:
                    domain = tldextract.extract(href).domain
                    if domain != tldextract.extract(has_link[i]).domain:
                        print(f"External favicon found: {href}")
                        result = 1
                    else:
                        print("External favicon not found")
                        result = 0
            email_features.append(result)
            # Extract InsecureForms
            for form in temp.find_all('form'):
                action = form.get('action')
                if action and not action.startswith("#"):
                    parsed_url = urlparse(action)
                    if parsed_url.scheme != "https":
                        print(f"Insecure form action found: {action}")
                        result = 1
                    else:
                        print("Insecure form action not found")
                        result = 0
            email_features.append(result)
            # Extract RelativeFormAction
            for form in temp.find_all('form'):
                action = form.get('action')
                if action and not action.startswith("#"):
                    parsed_url = urlparse(action)
                    if not parsed_url.scheme and not parsed_url.netloc:
                        print(f"Relative form action found: {action}")
                        result = 1
                    else:
                        print("Relative form action not found")
                        result = 0
            email_features.append(result)
            # Extract ExtFormAction
            for form in temp.find_all('form'):
                action = form.get('action')
                if action and not action.startswith("#"):
                    domain = tldextract.extract(action).domain
                    if domain != "example" and domain != "localhost":
                        print(f"External form action found: {action}")
                        result = 1
                    else:
                        print("External form action not found:")
                        result = 0
            email_features.append(result)
            # Extract AbnormalFormAction
            form_action = "about:blank"
            if not form_action:
                print("Empty form action")
                result = 1
            elif re.search(r"^javascript:true$", form_action):
                print("Form action contains javascript:true")
                result = 1
            elif re.search(r"^(#|about:blank)$", form_action):
                print("Form action contains # or about:blank")
                result = 1
            else:
                print("Normal form action")
                result = 0
            email_features.append(result)
            # Extract PctNullSelfRedirectHyperlinks
            total_links = 0
            null_self_redirect_links = 0
            for link in temp.find_all('a'):
                href = link.get('href')
                if href:
                    total_links += 1
                    if href == '#' or href == has_link[i] or href.startswith('file://'):
                        null_self_redirect_links += 1
            if total_links > 0:
                pct_null_self_redirect_links = (null_self_redirect_links / total_links) * 100
                print(f"Percentage of hyperlinks containing empty value, self-redirect value, or abnormal value: {pct_null_self_redirect_links:.2f}%")
                result = f"{pct_null_self_redirect_links:.2f}"
            else:
                print("No hyperlinks found in HTML")
                result = 0
            email_features.append(result)
            # Extract FrequentDomainNameMismatch
            links = [link.get("href") for link in temp.find_all("a")]
            url_domain = tldextract.extract(has_link[i]).domain
            domains = [tldextract.extract(link).domain for link in links]
            domain_counts = Counter(domains)
            most_frequent_domain = domain_counts.most_common(1)[0][0]
            if most_frequent_domain != url_domain:
                result = 1 
                print("Frequent domain name mismatch found")
            else:
                result = 0 
                print("Frequent domain name mismatch not found")
            email_features.append(result)
            # Extract FakeLinkInStatusBar
            if "onMouseOver" in html_content:
                result = 1 
                print("Fake link in status bar found")
            else:
                result = 0 
                print("Fake link in status bar not found")
            email_features.append(result)
            # Extract RightClickDisabled
            right_click_pattern = re.compile(r'document\.oncontextmenu\s*=\s*function\s*\(\s*\)\s*{\s*return\s+false;\s*}')
            right_click_disabled = bool(right_click_pattern.search(html_content))
            if right_click_disabled is True:
                result = 1
                print("Right_click_disabled: Yes")
            else:
                result = 0
                print("Right_click_disabled: No")
            email_features.append(result)
            # Extract PopUpWindow
            if "window.open" in html_content:
                result = 1
                print("PopUpWindow: Yes")
            else:
                result = 0
                print("PopUpWindow: No")
            email_features.append(result)
            # Extract SubmitInfoToEmail
            mailto_links = temp.find_all("a", href=lambda href: href and href.startswith("mailto:"))
            if mailto_links:
                result = 1
                print("SubmitInfoToEmail: Yes")
            else:
                result = 0
                print("SubmitInfoToEmail: No")
            email_features.append(result)
            # Extract IframeOrFrame
            iframes = temp.find_all('iframe')
            frames = temp.find_all('frame')
            if iframes or frames:
                result = 1
                print("Iframe or frame found")
            else:
                result = 0
                print("Iframe or frame not found")
            email_features.append(result)
            # Extract MissingTitle
            title = temp.find('title')
            if title and title.string:
                result = 1
                print("Title found")
            else:
                result = 0
                print("Title not found or empty")
            email_features.append(result)
            # Extract ImagesOnlyInForm
            forms = temp.find_all('form')
            for form in forms:
                if all([img.has_attr('src') for img in form.find_all('img')]) and not form.get_text().strip():
                    result = 1
                    print("Images only in form")
                else:
                    result = 0
                    print("Text found in form")
            email_features.append(result)
            # Extract SubdomainLevelRT
            subdomain_level = has_link[i].hostname.count('.')
            if subdomain_level == 1:
                print("Legitimate")
                result = 1
            elif subdomain_level == 2:
                print("Suspicious")
                result = 0
            elif subdomain_level > 2:
                print("Phishing")
                result = -1
            email_features.append(result)
            # Extract UrlLengthRT
            url_length = len(has_link[i])
            if url_length < 54:
                print("Legitimate")
                result = 1
            elif url_length >= 54 and url_length <= 75:
                print("Suspicious")
                result = 0
            else:
                print("Phishing")
                result = -1
            email_features.append(result)
            # Extract PctExtResourceUrlsRT
            try:
                response = requests.get(has_link[i], timeout=5)
                html = response.text
            except:
                print("Failed to download HTML source code")
                result = -1
            else:
                soup = BeautifulSoup(html, 'html.parser')
                total_resource_urls = 0
                external_resource_urls = 0
                for tag in soup.find_all(['img', 'link', 'script']):
                    url = tag.get('src') or tag.get('href')
                    if url and (url.startswith('http') or url.startswith('//')):
                        domain = tldextract.extract(url).domain
                        if domain != tldextract.extract(has_link[i]).domain:
                            external_resource_urls += 1
                        total_resource_urls += 1
                if total_resource_urls > 0:
                    pct_external_resource_urls = (external_resource_urls / total_resource_urls) * 100
                    if pct_external_resource_urls > 10:
                        result = 1
                    else:
                        result = 0
                else:
                    print("No resource URLs found in HTML")
                    result = -1
            print(f"Percentage of external resource URLs: {pct_external_resource_urls:.2f}%")
            print(f"Result: {result}")
            email_features.append(result)
            # Extract AbnormalExtFormActionR
            pattern = re.compile(r'<form.*?\saction=["\'](.*?)["\']', re.IGNORECASE | re.DOTALL)
            matches = pattern.findall(html_content)
            for match in matches:
                if "http" in match and "://" not in match[:10]:
                    result = 1
                    print("Has foreign domain")
                elif match.strip() == "about:blank" or not match.strip():
                    result = 1
                    print("Has about:blank, or empty string")
                else:
                    result = 0
                    print("Normal form action attribute")
            email_features.append(result)
            # Extract ExtMetaScriptLinkRT
            pattern = re.compile(r'(?:meta|script|link).*?\s(?:href|src)=["\'](http.*?)[&"\']', re.IGNORECASE | re.DOTALL)
            matches = pattern.findall(html_content)
            meta_count = 0
            script_count = 0
            link_count = 0
            for match in matches:
                if "http" not in match:
                    continue
                elif "javascript:" in match:
                    continue
                elif match.startswith("#"):
                    link_count += 1
                elif match.startswith("about:blank"):
                    link_count += 1
                elif match.startswith("file://"):
                    link_count += 1
                elif tldextract.extract(match).domain != tldextract.extract(has_link[i]).domain:
                    link_count += 1
                else:
                    if "meta" in match:
                        meta_count += 1
                    elif "script" in match:
                        script_count += 1
                    elif "link" in match:
                        link_count += 1
            total_count = meta_count + script_count + link_count
            if total_count == 0:
                result = 0
            else:
                meta_pct = meta_count / total_count
                script_pct = script_count / total_count
                link_pct = link_count / total_count
                if meta_pct >= 0.5:
                    result = 1
                elif script_pct >= 0.5:
                    result = 1
                elif link_pct >= 0.5:
                    result = 1
                elif link_pct >= 0.1:
                    result = -1
                else:
                    result = 0
            email_features.append(result)
            # Extract PctExtNullSelfRedirectHyperlinksRT
            pattern = re.compile(r'<a.*?href="(.*?)".*?>')
            matches = pattern.findall(html_content)
            external_links = 0
            null_links = 0
            self_redirect_links = 0
            for match in matches:
                if match == "" or match.startswith("#") or match.startswith("javascript::void(0)"):
                    null_links += 1
                elif has_link[i] not in match:
                    external_links += 1
                elif match == has_link[i] or match == has_link[i] +"/" or match == has_link[i] +"#":
                    self_redirect_links += 1
            total_links = len(matches)
            if total_links == 0:
                result = 0
            pct_null_links = null_links / total_links
            pct_external_links = external_links / total_links
            pct_self_redirect_links = self_redirect_links / total_links
            if pct_external_links > 0:
                result = 1
            elif pct_null_links > 0:
                result = -1
            else:
                result = 0
            email_features.append(result)

    #if there are no links, it's unlikely to be phishing (NOTE: 1 is phishing, 0 is not. I'm not keeping in the Class Label)
    else:
        email_features = {9820,2,1,2,45,0,0,0,0,0,0,0,0,0,0,
                          1,0,0,0,0,0,22,16,0,0,0,0,0.0583941606,0.1666666667,0,
                          0,0,0,0,0.0291970803,0,0,0,0,0,1,0,0,1,1,
                          1,1,0,1}
    # Combine the extracted features into a numpy array
    email_features = np.array(email_features)

    return email_features

def check_phishing(email_data):
    
    # Get the currently open email in Outlook
    #email_content = email_data

    # Preprocess the email content
    preprocessed_email_content = preprocess_email_content(email_data)
    print(preprocessed_email_content)

    # Transform the preprocessed email content into a format compatible with the random forest model
    email_features = transform_email_to_features(preprocessed_email_content)

    # RANDOM FOREST ALGORITHM
    # Load and preprocess the dataset
    print("Reading csv file...")
    features = pd.read_csv('src/Phishing_Legitimate_full.csv',sep=',')

    # split the data into label/target and features
    #aka y (THIS SHOULD BE OUR PHISHING/NOT PHISHING COLUMN)
    labels = np.array(features['CLASS_LABEL'])
    #aka x (This should be all of the features)
    features = features.drop('CLASS_LABEL', axis=1)

    #seperate the data into training and testing set
    train_features, test_features, train_labels, test_labels = train_test_split(features, labels, test_size=0.25, random_state=42)
    # Train the RandomForest model classify
    forest = RandomForestClassifier()
    forest.fit(train_features, train_labels)

    # Predict if the email is a phishing attempt using the random forest model
    #possibly change this back to without the reshape
    phishing_prediction = forest.predict(email_features.reshape(1, -1))

    # phishing prediction should output a lost of the features with it's pediction
    # of whether it's phishing or not
    # ex: [0 , 1, 0, 0, 0, 1, 0, 0, 0,..., 0]
    # Set a threshold for the prediction to classify it as phishing or not
    average = stats.mean(phishing_prediction)
    test = str(average)
    phishing_threshold = 0.5
    if average > phishing_threshold:
        print("This email may be a phishing attempt. Prediction: " + test)
        return "This is a phishing attempt. Report this immediately.  Prediction: " + test
    else:
        print("This email seems legitimate. Prediction: " + test)
        return "This is a legitimate. Prediction: " + test



