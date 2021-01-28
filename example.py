from SiteReview import SiteReview, WrongTLD

categorizer = SiteReview()
domain_names = ['google.com', 'youtube.com', 'dom.uu', 'facebook.com']
for domain in domain_names:
    try:
        cat = categorizer.get_category(domain, names_only=True)
        print(domain, cat)
    except WrongTLD:
        print(f'Wrong domain for {domain}')
        pass
