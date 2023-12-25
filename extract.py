# %%
import calendar
from urllib.parse import urlparse

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from selenium.webdriver.common.by import By
from seleniumbase import Driver
from tqdm import tqdm

from settings import cpl_password, cpl_username, output

# %%
driver = Driver(headless=True)

driver.get("https://calgary.bibliocommons.com/collection/show/my/library/completed")
driver.type("name", cpl_username, by="name")
driver.type("user_pin", cpl_password, by="name")
driver.click('input[name="commit"]')
driver.sleep(20)

last_page = driver.find_elements('a[data-key="page-link"]')[-1]
last_page_num = int(last_page.get_attribute("data-page"))
last_page_url = last_page.get_attribute("href")
q = urlparse(last_page_url).query
urls = [None] + [
    last_page_url.replace(q, f"page={i}") for i in range(2, last_page_num + 1)
]
urls

# %%
items = []
for url in tqdm(urls, desc="Extracting"):
    if url:
        driver.get(url)
        driver.sleep(10)

    books = driver.find_elements(".item-header")

    for book in books:
        title = book.find_element(By.CSS_SELECTOR, ".title-content").text
        try:
            author = book.find_element(By.CSS_SELECTOR, ".cp-author-link").text
        except:
            author = None
        date = book.find_element(By.CSS_SELECTOR, ".cp-short-formatted-date").text
        items.append((title, author, date))

# %%
df = pd.DataFrame(items)
df.columns = ["title", "author", "added date"]
df.to_csv(output / "data.csv", index=False)

# %%
df["added date"] = pd.to_datetime(df["added date"])
df["author"] = df["author"].apply(lambda v: " ".join(v.split(", ")[::-1]) if v else v)

# %%
summary1 = df.groupby(df["added date"].dt.year).count()[["title"]].reset_index()
summary1.columns = ["added year", "# of titles"]
summary1.to_csv(output / "summary-all-by-year.csv", index=False)
summary1

# %%
current = df[df["added date"].dt.year == df["added date"].dt.year.max()]
summary2 = current.groupby(df["added date"].dt.month).count()[["title"]].reset_index()
summary2.columns = ["added month", "# of titles"]
summary2.to_csv(output / "summary-current-by-month.csv", index=False)
summary2

# %%
summary3 = current.groupby(df["author"]).count()[["title"]].reset_index()
summary3.columns = ["author", "# of titles"]
summary3 = summary3.sort_values("# of titles", ascending=False).reset_index(drop=True)
summary3.to_csv(output / "summary-current-by-author.csv", index=False)
summary3

# %%
sns.set_style("whitegrid", {"grid.linestyle": "-."})

year = summary1["added year"].iloc[-1]
fig = plt.figure(figsize=(12, 12), constrained_layout=True)
fig.suptitle(f"CPL Year End Review {year}", fontsize=18, y=1.05)
gs = fig.add_gridspec(nrows=2, ncols=2)
ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[0, 1])
ax3 = fig.add_subplot(gs[1, :])

# ax1
pal = [sns.color_palette("Reds_r", summary1.shape[0])[-1]] * (summary1.shape[0] - 1) + [
    sns.color_palette("Reds_r", summary1.shape[0])[0]
]
ax = sns.barplot(
    data=summary1,
    x="added year",
    y="# of titles",
    palette=pal,
    hue="# of titles",
    ax=ax1,
)
total = summary1["# of titles"].iloc[-1]
ax.set_title(f"You read {total} books in {year}", {"fontsize": 14})

# ax2
ax = sns.barplot(
    data=summary2,
    x="added month",
    y="# of titles",
    palette=sns.color_palette("Reds_r", summary2["added month"].shape[0]),
    hue="# of titles",
    hue_order=summary2["# of titles"].sort_values(ascending=False).values,
    ax=ax2,
)
month = calendar.month_name[
    summary2[summary2["# of titles"] == summary2["# of titles"].max()][
        "added month"
    ].iloc[0]
]
ax.set_title(f"You read the most in {month}", {"fontsize": 14})

# ax3
num_authors = 9
ax = sns.barplot(
    data=summary3.head(num_authors),
    x="author",
    y="# of titles",
    palette=sns.color_palette("Reds_r", num_authors)[::-1],
    hue="# of titles",
    ax=ax3,
)
author = summary3.head(1)["author"].iloc[0]
ax.set_title(f"You read the most by {author}", {"fontsize": 14})
ax.set_xticklabels(ax.get_xticklabels(), fontsize=8, rotation=30)
ax.set_xlabel("")
fig.savefig(output / "year-end-review.png", bbox_inches="tight", dpi=300)

# %%
