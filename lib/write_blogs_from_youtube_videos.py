import os
import time
import sys

from pytube import YouTube
import tempfile
import openai
from html2image import Html2Image
from tqdm import tqdm, trange
from loguru import logger
logger.remove()
logger.add(sys.stdout,
        colorize=True,
        format="<level>{level}</level>|<green>{file}:{line}:{function}</green>| {message}"
    )

from .gpt_providers.openai_gpt_provider import openai_chatgpt, openai_chatgpt_streaming_text, speech_to_text


def youtube_to_blog(video_url):
    """Function to transcribe a given youtube url """
    # fixme: Doesnt work all types of yt urls.
    vid_id = video_url.split("=")[1]
    hti = Html2Image(output_path="../blog_images")
    hti.screenshot(url=video_url, save_as=f"yt-img-{vid_id}.png")
    yt_img_path = os.path.join("../blog_images", f"yt-img-{vid_id}.png")

    try:
        audio_text = speech_to_text(video_url)
        audio_blog_content = summarize_youtube_video(audio_text)
        return(yt_img_path, audio_blog_content)
    except Exception as e:
        logger.error(f"Error: Failed to transcribe YouTube video_url: {video_url} with error: {e}")


def summarize_youtube_video(user_content):
    """Generates a summary of a YouTube video using OpenAI GPT-3 and displays a progress bar.
    
    Args:
      video_link: The URL of the YouTube video to summarize.
    
    Returns:
      A string containing the summary of the video.
    """
    prompt = f"""
        You are an expert copywriter specializing in content optimization for SEO. 
        Your task is to transform a given transcript into a well-structured and engaging blog article. Your objectives include:

        1. Master the Transcript: Understand main ideas, key points, and the core message.
        2. Sentence Structure: Rephrase while preserving logical flow and coherence. Dont quote anyone from video.
        3. Identify Main Keywords: Determine the primary video topic.
        4. Keyword Integration: Naturally integrate keywords in headings, subheadings, and body text, avoiding overuse.
        5. Write Unique Content: Avoid direct copying; rewrite in your own words. 
           REMEMBER to avoid direct quoting and maintain uniqueness.
        6. Optimize for SEO: Implement meta tags, header tags, and appropriate keyword density.
        7. Craft Engaging and Informative Article: Provide value and insight to readers.
        8. Proofread: Check for grammar, spelling, and punctuation errors.
        9. Use Creative and Human-like Style: Incorporate contractions, idioms, transitional phrases, interjections, and colloquialisms. Avoid repetitive phrases and unnatural sentence structures.
        10. Structuring: Include a Creative Title, SEO Meta-description, ## Introduction ##, bullet points or numbered lists if appropriate, FAQs, and Conclusion.
        11. Ensure Uniqueness: Guarantee the article is plagiarism-free.
        12. Punctuation: Use appropriate question marks at the end of questions.
        13. Pass AI Detection Tools: Create content that easily passes AI plagiarism detection tools.
        14. Rephrase words like 'video, youtube, channel' with 'article, blog' and such suitable words.

        Follow the above guidelines to create a well-optimized, unique, and informative article that will rank well in search engine results and engage readers effectively.
        Craft a blog content from the following transcript:\n{user_content}
        """
    #completion_text = openai_chatgpt_streaming_text(prompt)
    completion_text = openai_chatgpt(prompt)
    return completion_text
