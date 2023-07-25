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
    # prev_date = None
    prev_year = set()
    for article in generator.articles:
        c_date = article.date.strftime("%b %d")
        set_str = c_date
        setattr(article, "monthdate", set_str)

        c_year_date = article.date.strftime("%Y")
        if c_year_date not in prev_year:
            prev_year.add(c_year_date)
            set_str = c_year_date
        else:
            set_str = None
        setattr(article, "yeardate", set_str)

        new_article.append(article)

    generator.articles = new_article
    # Update the context with the new list
    generator.context["articles"] = generator.articles


def register():
    signals.article_generator_finalized.connect(add_month_date_attr)
