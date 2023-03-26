<?php
    // Connect to the MySQL database
    include_once 'dbh.php';
    
    // Set the $mysqli variable to the $conn variable
    $mysqli = $conn;

// Check if the request method is POST
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $post = $_POST["course"];
    // Split the course data into an array of course codes
    $courses_taken = explode(',', $post);
    $eligible_courses = array();
    
    // Loop through each course code in the array of courses_taken
    foreach ($courses_taken as $course) {
        // Query the database to get all courses that have the current course code as a prerequisite
        $query = "SELECT * FROM courses_info WHERE prerequisites LIKE '%$course%'";
        $result = $mysqli->query($query);
        
        // Loop through each row returned by the query and add the course details to the eligible_courses array
        while ($row = $result->fetch_assoc()) {
            $course_details = array();
            $course_details['course_name'] = $row['course_name'];
            $course_details['program_area'] = $row['program_area'];
            $course_details['distribution_requirement'] = $row['distribution_requirement'];
            $course_details['exclusions'] = $row['exclusions'];
            $course_details['prerequisites'] = $row['prerequisites'];
            
            $course_code = $row['course_code'];
            
            // Add the course details to the eligible_courses array if the course code doesn't already exist in the array
            if (!array_key_exists($course_code, $eligible_courses)) {
                $eligible_courses[$course_code] = $course_details;
            }
        }
    }
    
    // Encode the eligible_courses array as JSON and echo it back to the index.html file
    echo json_encode($eligible_courses);
}
?>