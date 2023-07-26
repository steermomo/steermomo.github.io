"""
在每个article中添加archive_month_day和archive_year属性，用于在归档页面中显示文章的月份和年份
"""
from typing import List

from pelican import signals
from pelican.contents import Article
from pelican.generators import ArticlesGenerator


def add_month_date_attr(generator: ArticlesGenerator):
    new_article: List[Article] = []
    # count articles and keep the pinned ordered by date
    # prev_date = None
    prev_year = set()
    article: Article
    for article in generator.articles:
        c_date = article.date.strftime("%b %d")
        set_str = c_date
        setattr(article, "archive_month_day", set_str)

        c_year_date = article.date.strftime("%Y")
        if c_year_date not in prev_year:
            prev_year.add(c_year_date)
            set_str = c_year_date
        else:
            set_str = None
        setattr(article, "archive_year", set_str)

        new_article.append(article)

    generator.articles = new_article
    # Update the context with the new list
    generator.context["articles"] = generator.articles


def register():
    signals.article_generator_finalized.connect(add_month_date_attr)
