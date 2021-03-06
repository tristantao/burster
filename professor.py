
class Professor(object):

    def __init__(self, name, email, university_id, department):
        self.name = name
        self.email = email
        self.university_id = university_id
        self.department = department
        self.id = None

    def should_contact(self):
        #returns true if we're going to contact the Professor
        if not self.email:
            return False
        if Professor.bad_name_failure(self.email) or Professor.long_name_failure(self.email) \
        or Professor.non_alpha_subdomain_failure(self.email) or Professor.subdomain_length_failure(self.email) \
        or Professor.name_equal_domain_failure(self.email) or Professor.unfamilar_domain_failure(self.email):
            return False
        return True

    def cleaned_name(self):
        titles =["Dr.", "Mr.", "Ms.", "Mrs.", "Professor", "Professor.", "Prof", "Prof.", ","]
        if self.name:
            #output_name = re.sub(' +',' ', self.name)
            output_name = " ".join(self.name.split())
            for title in titles:
                output_name = output_name.replace(title, "")
            output_name = "".join([c for c in output_name if (c.isalpha() or c == " " or c == ".")])
            return "Dr. " + output_name.strip()
        else:
            return ""

    @staticmethod
    def unfamilar_domain_failure(sub_domain):
        good_domains = [".org", ".edu", ".com"]
        sub_domain = "".join(sub_domain.split("@")[1:]) if "@" in sub_domain else sub_domain
        for domain in good_domains:
            if domain in sub_domain:
                return False
        return True

    @staticmethod
    def name_equal_domain_failure(email):
        name = email.split("@")[0] if "@" in email else email
        sub_domain = "".join(email.split("@")[1:]) if "@" in email else email
        return name == sub_domain

    @staticmethod
    def subdomain_length_failure(sub_domain):
        sub_domain = "".join(sub_domain.split("@")[1:]) if "@" in sub_domain else sub_domain
        return len(sub_domain) <= 5 or len(sub_domain) > 25

    @staticmethod
    def non_alpha_subdomain_failure(sub_domain):
        sub_domain = "".join(sub_domain.split("@")[1:]) if "@" in sub_domain else sub_domain
        num_alpha = float(sum(1 for char in sub_domain if char.isalpha()))
        return (num_alpha / len(sub_domain) < 0.51)

    @staticmethod
    def long_name_failure(name):
        name = name.split("@")[0] if "@" in name else name
        return (len(name) > 20)

    @staticmethod
    def bad_name_failure(name):
         name_words_contains =  ['admission', 'spam', 'info', 'faculty', 'campus', 'webmaster', 'career', 'employment',
         'service', 'online', 'payroll', 'grads', 'news', 'publication', 'help', 'student', 'advisor', 'today', 'foundation',
         'search', 'physics', 'stats', 'math', 'german', 'name', 'phd', 'associate']
         name_words_exact = ['news', 'foo', 'you', 'phys', 'theatre', 'theater', 'hr', "%"]
         name = name.split("@")[0] if "@" in name else name
         for taboo_contains in name_words_contains:
             if taboo_contains in name:
                 return True
         return False if name not in name_words_exact else True

if __name__ == "__main__":
    test_professor1 = Professor('name', 'student@legit.com', 'university_id', 'department')
    print test_professor1.should_contact()
    test_professor2 = Professor('Dr. Tao', 'student@legit.com', 'university_id', 'department')
    print test_professor2.cleaned_name()
    test_professor3 = Professor('Dr. Tao', 'lam@humber.ca', 'university_id', 'department')
    print test_professor3.should_contact()

