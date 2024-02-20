"""
Pin to top plugin for Pelican
================================
Adds .pin variable to article's context and pins the article to the top
 even if it is older than the other articles
"""
from pelican import signals
from pelican.contents import Content
from pelican.generators import ArticlesGenerator


def update_pinned_articles(generator: ArticlesGenerator):
    new_order = []
    # count articles and keep the pinned ordered by date
    pinned = 0
    article: Content
    for article in generator.articles:
        if hasattr(article, "pin"):
            new_order.insert(pinned, article)
            pinned += 1
        else:
            new_order.append(article)
    generator.articles = new_order
    # Update the context with the new list
    generator.context["articles"] = generator.articles


def register():
    signals.article_generator_finalized.connect(update_pinned_articles)
