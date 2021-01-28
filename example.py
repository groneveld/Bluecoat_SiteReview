from SiteReview import SiteReview, Wrong_TLD

categorizer = SiteReview()
domain_names = ['google.com', 'youtube.com', 'dom.uu']
for domain in domain_names:
    try:
        cat = categorizer.get_category(domain, names_only=True)
        print(domain, cat)
    except Wrong_TLD:
        print(f'Wrong domain for {domain}')
        pass
