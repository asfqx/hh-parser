class Search:
    def __init__(self):
        self.text = ""
        self.age_from = ""
        self.age_to = ""
        self.label = "only_with_age"
        self.employment = ""
        self.experience = ""
        self.gender = ""
        self.order_by = "relevance"
        self.vacancy_id = ""
        self.education_level = ""
        self.url = ""

    def generate_search_link(self):
        url = f"https://api.hh.ru/resumes?label={self.label}&order_by={self.order_by}"
        for text in self.text.split():
            url = url + f"&text={text}"
        if self.age_from:
            url = url + f"&age_from={self.age_from}"
            if self.age_to:
                url = url + f"&age_to={self.age_to}"
        if self.employment:
            url = url + f"&employment={self.employment}"
        if self.experience:
            url = url + f"&experience={self.experience}"
        if self.gender:
            url = url + f"&gender={self.gender}"
        if self.vacancy_id:
            url = url + f"&vacancy_id={self.vacancy_id}"
        if self.education_level:
            url = url + f"&education_levels={self.education_level}"
        self.url = url


search = Search()
