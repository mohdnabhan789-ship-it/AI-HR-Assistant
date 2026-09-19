from sentence_transformers import SentenceTransformer
import faiss


# --------------------------------
# 1. HR Policy
# --------------------------------

hr_policy = """
HR POLICY

Annual Leave:
Employees receive 24 days of annual leave per year.

Sick Leave:
Employees can take up to 12 days of sick leave per year.

Work From Home:
Employees can work from home up to 2 days per week with manager approval.

Working Hours:
Standard working hours are 9:00 AM to 6:00 PM, Monday to Friday.

Salary:
Employees receive their salary at the end of each month.
"""


# --------------------------------
# 2. Create embedding model
# --------------------------------

model = SentenceTransformer("all-MiniLM-L6-v2")


# --------------------------------
# 3. Convert policy into embedding
# --------------------------------

policy_embedding = model.encode([hr_policy])


# --------------------------------
# 4. Create FAISS index
# --------------------------------

dimension = policy_embedding.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(policy_embedding)


# --------------------------------
# 5. Search HR policy
# --------------------------------

def search_hr_policy(question):

    question_embedding = model.encode([question])

    distance, result = index.search(
        question_embedding,
        k=1
    )

    return hr_policy