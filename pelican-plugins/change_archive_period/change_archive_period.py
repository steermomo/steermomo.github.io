"""
Pin to top plugin for Pelican
================================
Adds .pin variable to article's context and pins the article to the top
 even if it is older than the other articles
"""
from pelican import signals

def add_month_date_attr(generator):
    new_article = []
    # count articles and keep the pinned ordered by date
    prev_date = None
    
    for article in generator.articles:
        c_date = article.date.strftime('%b %Y')
        if prev_date is None or prev_date != c_date:
            prev_date = c_date
            set_str = prev_date
        else:
            set_str = ''    
        setattr(article, 'monthdate', set_str)
        
        new_article.append(article)

    generator.articles = new_article
    # Update the context with the new list
    generator.context['articles'] = generator.articles

def register():
    signals.article_generator_finalized.connect(add_month_date_attr)