import asyncio
from io import BytesIO
from urllib.parse import urlsplit, urlunsplit

import httpx


TIMEOUT = 30

HEADERS = {
    "User-Agent": (
        "TelegramAutomations/1.0 "
        "(personal historical content project)"
    ),
    "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/png,image/jpeg,*/*",
}


def clean_image_url(
    image_url: str,
) -> str:

    """
    Remove tracking parameters from Wikimedia URLs.

    Example:
    ?utm_source=en.wikipedia.org
    """

    parsed = urlsplit(image_url)

    return urlunsplit(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path,
            "",
            "",
        )
    )


def detect_extension(
    content_type: str,
    url: str,
) -> str:

    content_type = (
        content_type
        .lower()
        .split(";")[0]
        .strip()
    )

    if content_type == "image/jpeg":
        return "jpg"

    if content_type == "image/png":
        return "png"

    if content_type == "image/webp":
        return "webp"

    if content_type == "image/gif":
        return "gif"

    if content_type == "image/avif":
        return "avif"

    if content_type == "image/svg+xml":
        return "png"

    path = (
        urlsplit(url)
        .path
        .lower()
    )

    if path.endswith(".jpg"):
        return "jpg"

    if path.endswith(".jpeg"):
        return "jpg"

    if path.endswith(".png"):
        return "png"

    if path.endswith(".webp"):
        return "webp"

    if path.endswith(".gif"):
        return "gif"

    return "jpg"


async def download_image(
    image_url: str | None,
) -> tuple[bytes | None, str | None]:

    if not image_url:
        return None, None

    url = clean_image_url(
        image_url
    )

    last_error = None

    async with httpx.AsyncClient(
        timeout=TIMEOUT,
        follow_redirects=True,
        headers=HEADERS,
    ) as client:

        for attempt in range(3):

            try:

                response = await client.get(
                    url
                )

                response.raise_for_status()

                content = response.content

                if not content:
                    raise ValueError(
                        "Image response was empty."
                    )

                content_type = (
                    response.headers.get(
                        "content-type",
                        "",
                    )
                )

                extension = detect_extension(
                    content_type,
                    url,
                )

                # Basic validation.
                #
                # This prevents HTML error pages from
                # accidentally being treated as images.
                if (
                    content.startswith(
                        b"<html"
                    )
                    or content.startswith(
                        b"<!DOCTYPE"
                    )
                ):
                    raise ValueError(
                        "Server returned HTML instead "
                        "of an image."
                    )

                return (
                    content,
                    extension,
                )

            except (
                httpx.HTTPError,
                ValueError,
            ) as error:

                last_error = error

                if attempt < 2:

                    await asyncio.sleep(
                        1.5 * (attempt + 1)
                    )

    print(
        f"Image download failed: {last_error}"
    )

    return None, None