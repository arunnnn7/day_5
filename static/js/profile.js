$(document).ready(function() {

    // 1. Live Time using JavaScript (updates every second)
    function showCurrentTime() {
        let currentTime = new Date().toLocaleTimeString();
        $('#live-clock').text(currentTime);
    }
    showCurrentTime();
    setInterval(showCurrentTime, 1000);


    // 2. jQuery Toggle button: "Show/Hide Details"
    $('#toggle-details-btn').click(function() {
        $('#student-details-card').slideToggle(300, function() {
            if ($('#student-details-card').is(':visible')) {
                $('#toggle-details-btn').text('Hide Details');
            } else {
                $('#toggle-details-btn').text('Show Details');
            }
        });
    });


    // 3. Dropdown to update course using AJAX (jQuery $.post)
    $('#update-course-dropdown').change(function() {
        let selectedCourse = $(this).val();

        if (!selectedCourse) {
            return;
        }

        // Send POST request to /update-course
        $.post('/update-course', { course: selectedCourse }, function(response) {
            if (response.success) {
                // Update course text in the profile view
                $('#profile-course-text').text(selectedCourse);

                // Show alert as required by assessment
                alert('Course updated to: ' + selectedCourse);

                // Show toast notification
                $('#toast').text('Course updated to: ' + selectedCourse).fadeIn().delay(2500).fadeOut();
            } else {
                alert('Failed to update course: ' + (response.message || 'Error'));
            }
        }).fail(function() {
            alert('Error updating course in database.');
        });
    });

});
