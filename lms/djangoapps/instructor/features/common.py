"""
Define common steps for instructor dashboard acceptance tests.
"""

# pylint: disable=C0111
# pylint: disable=W0621

from __future__ import absolute_import

from lettuce import world, step
from nose.tools import assert_in  # pylint: disable=E0611

from courseware.tests.factories import StaffFactory, InstructorFactory


@step(u'Given I am "([^"]*)" for a course')
def i_am_staff_or_instructor(step, role):  # pylint: disable=unused-argument
    ## In summary: makes a test course, makes a new Staff or Instructor user
    ## (depending on `role`), and logs that user in to the course

    # Store the role
    assert_in(role, ['instructor', 'staff'])

    # Clear existing courses to avoid conflicts
    world.clear_courses()

    # Create a new course
    course = world.CourseFactory.create(
        org='edx',
        number='999',
        display_name='Test Course'
    )

    world.course_id = 'edx/999/Test_Course'
    world.role = 'instructor'
    # Log in as the an instructor or staff for the course
    if role == 'instructor':
        # Make & register an instructor for the course
        world.instructor = InstructorFactory(course=world.course_id)
        world.enroll_user(world.instructor, world.course_id)

        world.log_in(
            username=world.instructor.username,
            password='test',
            email=world.instructor.email,
            name=world.instructor.profile.name
        )

    else:
        world.role = 'staff'
        # Make & register a staff member
        world.staff = StaffFactory(course=course.location)
        world.enroll_user(world.staff, world.course_id)

        world.log_in(
            username=world.staff.username,
            password='test',
            email=world.staff.email,
            name=world.staff.profile.name
        )


def go_to_section(section_name):
    # section name should be one of
    # course_info, membership, student_admin, data_download, analytics, send_email
    world.visit('/courses/edx/999/Test_Course')
    world.css_click('a[href="/courses/edx/999/Test_Course/instructor"]')
    world.css_click('div.beta-button-wrapper>a')
    world.css_click('a[data-section="{0}"]'.format(section_name))


@step(u'I click "([^"]*)"')
def click_a_button(step, button):  # pylint: disable=unused-argument

    if button == "Generate Grade Report":
        # Go to the data download section of the instructor dash
        go_to_section("data_download")

        # Click generate grade report button
        world.css_click('input[name="calculate-grades-csv"]')

        # Expect to see a message that grade report is being generated
        expected_msg = "Your grade report is being generated! You can view the status of the generation task in the 'Pending Instructor Tasks' section."
        world.wait_for_visible('#grade-request-response')
        assert_in(
            expected_msg, world.css_text('#grade-request-response'),
            msg="Could not find grade report generation success message."
        )

    elif button == "Grading Configuration":
        # Go to the data download section of the instructor dash
        go_to_section("data_download")

        world.css_click('input[name="dump-gradeconf"]')

    elif button == "List enrolled students' profile information":
        # Go to the data download section of the instructor dash
        go_to_section("data_download")

        world.css_click('input[name="list-profiles"]')

    else:
        raise ValueError("Unrecognized button option " + button)
