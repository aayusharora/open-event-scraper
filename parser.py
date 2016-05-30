import saveImage
import saveAudio

# result is a dictionary of the excel sheet
def get_linkedin_url(result):
    if result.has_key("linkedin"):
        return result["linkedin"]
    elif result.has_key("Linkedin"):
        return result["Linkedin"]
    elif result.has_key("LinkedIn"):
        return result["LinkedIn"]
    elif result.has_key("linkedIn"):
        return result["linkedIn"]
    return ""


def get_pic_url(result):
    if result.has_key("Photo for Website and Program"):
        return result["Photo for Website and Program"]
    elif result.has_key("image"):
        return result["image"]
    elif result.has_key("Please add a link to a color photo - of You - in good quality we can use for the website."):
        img_url = result["Please add a link to a color photo - of You - in good quality we can use for the website."]
        filename = result["Given Name"].replace("/","_") + "_" + result["Family Name"].replace("/","_") + ".jpg"
        return saveImage.save_img(img_url, filename)
    return ""

def get_audio_url(aud_url):
    filename = aud_url.rsplit('/', 1)[-1]
    return saveAudio.save_audio(aud_url, filename)
