from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment

from .schema import AssignmentSchema, AssignmentSubmitSchema, AssignmentGradeSchema
teacher_assignments_resources = Blueprint('teacher_assignments_resources', __name__)


# Get all the assignments submitted to a specific teacher
@teacher_assignments_resources.route('/assignments',methods=['GET'],strict_slashes=False)
@decorators.auth_principal
def list_assignments(p):
    
    students_assignments = Assignment.get_assignments_of_teacher(p.teacher_id)
    students_assignments_dump = AssignmentSchema().dump(students_assignments, many=True)
    return APIResponse.respond(data=students_assignments_dump)


# Grade an Assignment
@teacher_assignments_resources.route('/assignments/grade',methods=['POST'],strict_slashes=False)
@decorators.accept_payload
@decorators.auth_principal
def grade_assignment(p,incoming_payload):
    
    # First Deserialize the JSON Formatted Data into the Python Readable Format (Key-Value Pair Custom Object)
    graded_assignment_payload = AssignmentGradeSchema().load(incoming_payload)
    
    # Took the necessary values from the deserialized object payload and pass into the controller
    graded_assignment = Assignment.grade_the_assignment(
        _id = graded_assignment_payload.id,
        grade = graded_assignment_payload.grade,
        principal=p
    )
    db.session.commit()
    graded_assignment_dump = AssignmentSchema().dump(graded_assignment)
    return APIResponse.respond(data=graded_assignment_dump)