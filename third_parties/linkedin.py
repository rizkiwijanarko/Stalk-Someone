import os
import requests
from dotenv import load_dotenv

load_dotenv()

def scrape_linkedin_profile(profile_url : str, mock : bool = False):
    """
    Scrape a LinkedIn profile for information
    """

    if mock:
        profile_url = "https://gist.githubusercontent.com/rizkiwijanarko/2315fbb8275490d7c311c9eaffe64e5c/raw/99c3d1be6b35ccd8c476b7eb1f247c51acb0b6f4/rizki-wijanarko.json"
        response = requests.get(
            profile_url,
            timeout=10
        )
    else:
        api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"
        headers = {'Authorization': f"Bearer {os.getenv('PROXYCURL_API_KEY')}"}
        response = requests.get(
            api_endpoint,
            params={"url": profile_url},
            headers=headers,
            timeout=10
        )

    data = response.json()

    data = {
        k: v for k, v in data.items()
        if v not in ([], "", "", None)
        and k not in ["people_also_viewed", "certifications"]
    }

    if data.get("groups"):
        for group_dict in data.get("groups"):
            group_dict.pop("profile_pic_url")

    return data


if __name__ == "__main__":
    print(
        scrape_linkedin_profile(
            "https://www.linkedin.com/in/rizki-wijanarko/", mock=True
        )
    )