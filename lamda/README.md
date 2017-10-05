ClassSession:
  - term  (str) 1, 2, 1-2
  - day   (str) Mon, Tue, Wed, Thu, Fri, Sat, Sun
  - start (str) [00-24]:[00-60] e.g. 14:30
  - end   (str) [00-24]:[00-60] e.g. 14:30

Course:
  - name (str) <DEPT> <LEVEL> <SECTION> e.g. MATH 100 102
  - class_sessions (list<ClassSession>)

a 'schedule' is a list<Course>
