from pyknow import *
import streamlit as st
results=[]
class Personne(Fact):
    pass

def SUMFIELDS(p, *fields):
    return sum([p.get(x, 0) for x in fields])

class InreferenceEngine(KnowledgeEngine):
    @Rule(Personne(age=P(lambda x: x <= 5)))
    def concerned_person(self):
        self.declare(Fact(concerned=True))

    @Rule(Fact(concerned=True),
          Personne(glycemie=MATCH.glycemie))
    def hyper_glycemy(self, glycemie):
        if glycemie > 10:
            self.declare(Fact(hyperglycemic_risk=True))
            st.text("Warning! High blood sugar")
        else:
            self.declare(Fact(hyperglycemic_risk=False))

    @Rule(Fact(concerned=True),
          Personne(glycemie=MATCH.glycemie))
    def hypo_glycemy(self, glycemie):
        if glycemie < 4:
            st.text("Warning! Low blood sugar")
            self.declare(Fact(hypoglycemic_risk=True))
        else:
            self.declare(Fact(hypoglycemic_risk=False))

    @Rule(Fact(concerned=True),
          AS.p << Personne(),
          TEST(lambda p: SUMFIELDS(p,
                                   'shakiness',
                                   'hunger',
                                   'sweating',
                                   'headach',
                                   'pale') > 2))
    def has_signs_low_sugar(self, p):
        self.declare(Fact(has_signs_low_sugar=True))

    @Rule(Fact(concerned=True),
          Fact(has_diabetic_parents=True),
          Fact(has_signs_low_sugar=True))
    def protocole_risk_low(self):
        st.text("Warning! Child could be diabetic")

    @Rule(Fact(concerned=True),
          Fact(hypoglycemic_risk=True),
          Fact(has_signs_low_sugar=True))
    def protocole_alert_low(self):
        st.text("Alert! High risk of diabetes, you must see a doctor")

    @Rule(Fact(concerned=True),
          Personne(diabetic_parents=True))
    def has_diabetic_parents(self):
        self.declare(Fact(has_diabetic_parents=True))

    @Rule(Fact(concerned=True),
          AS.p << Personne(),
          TEST(lambda p: SUMFIELDS(p,
                                   'urination',
                                   'thirst',
                                   'blurred_vision',
                                   'headach',
                                   'dry_mouth',
                                   'smelling_breath',
                                   'shortness_of_breath') > 2)
    )
    def has_signs_high_sugar(self, **_):
        self.declare(Fact(has_signs_high_sugar=True))

    @Rule(Fact(concerned=True),
          Fact(has_diabetic_parents=True),
          Fact(has_signs_high_sugar=True))
   

    @Rule(Fact(concerned=True),
          Fact(hyperglycemic_risk=True),
          Fact(has_signs_high_sugar=True))
    def protocole_alert_high(self):
        st.text("Alert! High risk of diabetes, you must see a doctor")

engine = InreferenceEngine()
st.title("Medical Diagnosis")

# Input form
age = st.slider("Select age:", 0, 100, 18)
glycemie = st.slider("Select glycemie:", 0, 20, 5)
shakiness = st.checkbox("Shakiness")
hunger = st.checkbox("Hunger")
sweating = st.checkbox("Sweating")
headach = st.checkbox("Headach")
diabetic_parents = st.checkbox("Diabetic Parents")
pale = st.checkbox("Pale")
urination = st.checkbox("Urination")
thirst = st.checkbox("Thirst")
blurred_vision = st.checkbox("Blurred Vision")
dry_mouth = st.checkbox("Dry Mouth")
smelling_breath = st.checkbox("Smelling Breath")
shortness_of_breath = st.checkbox("Shortness of Breath")

# Run the engine on button click
if st.button("Run Diagnosis"):
    engine.reset()
    person_fact = Personne(age=age,
                            glycemie=glycemie,
                            shakiness=shakiness,
                            hunger=hunger,
                            sweating=sweating,
                            headach=headach,
                            diabetic_parents=diabetic_parents,
                            pale=pale,
                            urination=urination,
                            thirst=thirst,
                            blurred_vision=blurred_vision,
                            dry_mouth=dry_mouth,
                            smelling_breath=smelling_breath,
                            shortness_of_breath=shortness_of_breath)
    engine.declare(person_fact)
    for i in results:
        st.text(i)
    engine.run()