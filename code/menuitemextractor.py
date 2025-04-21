if __name__ == "__main__":
    import sys
    sys.path.append('code')
    from menuitem import MenuItem
else:
    from code.menuitem import MenuItem


def clean_price(price: str) -> float:
    cleaned = price.replace("$", "").replace(",", "").strip()
    return float(cleaned)

def clean_scraped_text(scraped_text: str) -> list[str]:
    lines = scraped_text.split("\n")
    ignore = {"", "NEW", "NEW!", "S", "V", "GS", "P"}
    return [line.strip() for line in lines if line.strip() not in ignore]

def extract_menu_item(title: str, scraped_text: str) -> MenuItem:
    cleaned = clean_scraped_text(scraped_text)
    
    name = cleaned[0]
    price = clean_price(cleaned[1])
    description = cleaned[2] if len(cleaned) > 2 else "No description available"
    
    return MenuItem(category=title, name=name, price=price, description=description)

if __name__=='__main__':
    pass
