#!/usr/bin/env python3
from bs4 import BeautifulSoup
from urllib import request
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlparse, urlunparse
import argparse
import random
import sys


def crawl(website):
    found_broken_link = False
    seen_links = set()
    links_to_crawl = [website]

    while links_to_crawl:
        link = links_to_crawl.pop(0)
        try:
            response = request.urlopen(link)
            redirected_website = response.geturl()
            html = response.read().decode()
        except HTTPError as e:
            print("💔 {} didn't work! ({})".format(link, e))
            found_broken_link = True
        except URLError:
            # in case this is a url urllib doesn't understand (like mailto:), just ignore it
            pass
        else:
            print("🙂 {} worked".format(link))

        soup = BeautifulSoup(html, "html.parser")

        # limit crawling to specified website
        if redirected_website.startswith(website):
            for link in soup.find_all("a"):
                href = link.get("href")
                if href:
                    href = urljoin(redirected_website, link.get("href"))
                    href = urlunparse(urlparse(href)[:-1] + ("",))  # strip query string
                    if href not in seen_links:
                        links_to_crawl.append(href)
                        seen_links.add(href)

    return found_broken_link


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check links")
    parser.add_argument("website")
    args = parser.parse_args()

    broken_links = crawl(args.website)
    print()

    if broken_links:
        print("💥 Broken links make me sad 😢")
        sys.exit(1)
    else:
        animals = (
            ("🐵", "Monkey"),
            ("🐒", "Monkey"),
            ("🦍", "Gorilla"),
            ("🐶", "Dog Face"),
            ("🐕", "Dog"),
            ("🐩", "Poodle"),
            ("🐺", "Wolf"),
            ("🦊", "Fox"),
            ("🦝", "Raccoon"),
            ("🐱", "Cat"),
            ("🐈", "Cat"),
            ("🦁", "Lion"),
            ("🐯", "Tiger"),
            ("🐅", "Tiger"),
            ("🐆", "Leopard"),
            ("🐴", "Horse"),
            ("🐎", "Horse"),
            ("🦄", "Unicorn"),
            ("🦓", "Zebra"),
            ("🐮", "Cow"),
            ("🐃", "Water Buffalo"),
            ("🐄", "Cow"),
            ("🐷", "Pig"),
            ("🐖", "Pig"),
            ("🐗", "Boar"),
            ("🐏", "Ram"),
            ("🐑", "Sheep"),
            ("🐐", "Goat"),
            ("🐪", "Camel"),
            ("🐫", "Two-Hump Camel"),
            ("🦙", "Llama"),
            ("🦒", "Giraffe"),
            ("🐘", "Elephant"),
            ("🦏", "Rhinoceros"),
            ("🦛", "Hippopotamus"),
            ("🐭", "Mouse"),
            ("🐁", "Mouse"),
            ("🐀", "Rat"),
            ("🐹", "Hamster"),
            ("🐰", "Rabbit"),
            ("🐇", "Rabbit"),
            ("🐿", "Chipmunk"),
            ("🦔", "Hedgehog"),
        )
        animal = random.choice(animals)
        print(
            "🎆 No broken links! As a reward here's a {}: {}".format(
                animal[1].lower(), animal[0]
            )
        )
        sys.exit(0)
