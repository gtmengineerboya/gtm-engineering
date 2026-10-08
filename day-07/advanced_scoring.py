# def calculate_score(company):

#     score = 0

#     # Industry — 25 points
#     if company["industry"] == "SaaS":
#         score += 25

#     # Company size — 20 points
#     if int(company["employees"]) >= 500:
#         score += 20

#     # US location — 15 points
#     if company["country"] == "USA":
#         score += 15

#     return score


# company = {
#     "company": "Acme AI",
#     "industry": "SaaS",
#     "employees": 750,
#     "country": "USA"
# }

# score = calculate_score(company)

# print("Company:", company["company"])
# print("ICP Score:", score)



# def calculate_score(company):

#     score = 0

#     # Industry — 25 points
#     if company["industry"] == "SaaS":
#         score += 25

#     # Company size — 20 points
#     if int(company["employees"]) >= 500:
#         score += 20

#     # US location — 15 points
#     if company["country"] == "USA":
#         score += 15

#     # Job title — 20 points
#     target_titles = [
#         "CEO",
#         "CTO",
#         "VP Sales",
#         "VP Marketing",
#         "Chief Growth Officer",
#         "Revenue Operations Manager"
#     ]

#     if company["job_title"] in target_titles:
#         score += 20

#     # Technology — 10 points
#     target_technologies = [
#         "AWS",
#         "Azure",
#         "GCP",
#         "Kubernetes"
#     ]

#     technologies = company["technology"].split(";")
#     #For every tech in technologies, check whether that tech is in target_technologies.
#     if any(tech in target_technologies for tech in technologies):#If at least one technology in this company is present in our target technology list, run the if block.
#         score += 10

#     # Buying signal — 10 points
#     if company["buying_signal"] == "Demo Request":
#         score += 10

#     return score


# company = {
#     "company": "Acme AI",
#     "industry": "SaaS",
#     "employees": 750,
#     "country": "USA",
#     "job_title": "VP Sales",
#     "technology": "AWS;Python;React",
#     "buying_signal": "Demo Request"
# }

# score = calculate_score(company)

# print("Company:", company["company"])
# print("ICP Score:", score)


# ---------------------------------
# 1. Calculate ICP Score
# ---------------------------------

def calculate_score(company):

    score = 0

    # Industry — 25 points
    if company["industry"] == "SaaS":
        score += 25

    # Company size — 20 points
    if int(company["employees"]) >= 500:
        score += 20

    # US location — 15 points
    if company["country"] == "USA":
        score += 15

    # Job title — 20 points
    target_titles = [
        "CEO",
        "CTO",
        "VP Sales",
        "VP Marketing",
        "Chief Growth Officer",
        "Revenue Operations Manager"
    ]

    if company["job_title"] in target_titles:
        score += 20

    # Technology — 10 points
    target_technologies = [
        "AWS",
        "Azure",
        "GCP",
        "Kubernetes"
    ]

    technologies = company["technology"].split(";")

    if any(tech in target_technologies for tech in technologies):
        score += 10

    # Buying signal — 10 points
    if company["buying_signal"] == "Demo Request":
        score += 10

    return score #we take this value directly into --->test_scoring.py file


# ---------------------------------
# 2. Explain ICP Score
# ---------------------------------

def explain_score(company):

    reasons = []

    if company["industry"] == "SaaS":
        reasons.append("SaaS industry: +25")

    if int(company["employees"]) >= 500:
        reasons.append("500+ employees: +20")

    if company["country"] == "USA":
        reasons.append("USA location: +15")

    target_titles = [
        "CEO",
        "CTO",
        "VP Sales",
        "VP Marketing",
        "Chief Growth Officer",
        "Revenue Operations Manager"
    ]

    if company["job_title"] in target_titles:
        reasons.append("Target job title: +20")

    target_technologies = [
        "AWS",
        "Azure",
        "GCP",
        "Kubernetes"
    ]

    technologies = company["technology"].split(";")

    if any(tech in target_technologies for tech in technologies):
        reasons.append("Target technology match: +10")

    if company["buying_signal"] == "Demo Request":
        reasons.append("Demo request buying signal: +10")

    return reasons


# ---------------------------------
# 3. Test Company
# ---------------------------------

company = {
    "company": "Acme AI",
    "industry": "SaaS",
    "employees": 750,
    "country": "USA",
    "job_title": "VP Sales",
    "technology": "AWS;Python;React",
    "buying_signal": "Demo Request"
}


# ---------------------------------
# 4. Calculate Score
# ---------------------------------

score = calculate_score(company)


# ---------------------------------
# 5. Get Score Explanation
# ---------------------------------

reasons = explain_score(company)


# ---------------------------------
# 6. Display Results
# ---------------------------------

print("================================")
print("GTM ICP SCORING")
print("================================")

print("Company:", company["company"])
print("ICP Score:", score, "/ 100")

print("\nWhy this lead received", score, "/ 100:")

for reason in reasons:
    print("-", reason)