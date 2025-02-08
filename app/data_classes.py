class Service:
    def __init__(self, name, description):
        self.name = name
        self.description = description


class News:
    def __init__(self, image, title, date, description, link, content):
        self.image = image
        self.title = title
        self.date = date
        self.description = description
        self.link = link
        self.content = content


class Manager:
    def __init__(self, name, position, image, phone_url, mail_url, linkedin_url):
        self.name = name
        self.position = position
        self.image = image
        self.phone_url = phone_url
        self.mail_url = mail_url
        self.linkedin_url = linkedin_url


class Value:
    def __init__(self, title, icon, alt, description):
        self.title = title
        self.icon = icon
        self.alt = alt
        self.description = description


class Vacancy:
    def __init__(self, id, title, localization, job_description, requirements, recruiter_email, recruiter_name):
        self.id = id
        self.title = title
        self.localization = localization
        self.job_description = job_description
        self.requirements = requirements
        self.recruiter_email = recruiter_email
        self.recruiter_name = recruiter_name
