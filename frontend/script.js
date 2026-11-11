
const API_URL = "/employees";

// Load employees from Flask
async function loadEmployees() {
    try {
        const response = await fetch(API_URL);

        if (!response.ok) {
            throw new Error("Failed to load employees");
        }

        const employees = await response.json();

        // Update employee count
        document.getElementById("employeeCount").textContent =
            employees.length;

        // Find the employee table
        const table = document.getElementById("employeeTable");

        // Clear old table rows
        table.innerHTML = "";

        // Display each employee
        employees.forEach(employee => {
            const row = document.createElement("tr");

            const idCell = document.createElement("td");
            idCell.textContent = employee.id;

            const nameCell = document.createElement("td");
            nameCell.textContent = employee.name;

            const departmentCell = document.createElement("td");
            departmentCell.textContent = employee.department;

            
const actionsCell = document.createElement("td");

// Create Edit button
const editButton = document.createElement("button");

editButton.textContent = "Edit";
editButton.className = "edit-btn";

// When Edit is clicked
editButton.addEventListener("click", function () {

    // Store the employee ID
    document.getElementById("employeeId").value =
        employee.id;

    // Fill the form with existing employee details
    document.getElementById("employeeName").value =
        employee.name;

    document.getElementById("employeeDepartment").value =
        employee.department;

    // Change Save button to Update
    document.getElementById("submitButton").textContent =
        "Update Employee";

    // Scroll to the form
    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });
});

// Display the Edit button in the table
actionsCell.appendChild(editButton);

// Create Delete button
const deleteButton = document.createElement("button");

deleteButton.textContent = "Delete";
deleteButton.className = "delete-btn";

// Handle Delete button click
deleteButton.addEventListener("click", async function () {

    // Ask for confirmation before deleting
    const confirmed = confirm(
        `Are you sure you want to delete ${employee.name} (ID: ${employee.id})?`
    );

    if (!confirmed) {
        return;
    }

    try {
        // Send DELETE request to Flask
        const response = await fetch(
            `${API_URL}/${employee.id}`,
            {
                method: "DELETE"
            }
        );

        if (!response.ok) {
            throw new Error("Failed to delete employee");
        }

        alert("Employee deleted successfully!");

        // Refresh the employee table
        await loadEmployees();

    } catch (error) {
        console.error("Error:", error);
        alert("Unable to delete employee.");
    }
});

// Display Delete button beside Edit
actionsCell.appendChild(deleteButton);



            row.append(
                idCell,
                nameCell,
                departmentCell,
                actionsCell
            );

            table.appendChild(row);
        });

    } catch (error) {
        console.error("Error:", error);
        alert("Unable to load employees. Check the Flask server.");
    }
}

// Load employees when the page opens
loadEmployees();

// Handle the Add Employee form
document.getElementById("employeeForm")
    .addEventListener("submit", async function (event) {

        // Prevent the browser from reloading the page
        event.preventDefault();

        // Get values entered by the user
        const name = document.getElementById("employeeName")
            .value.trim();

        const department = document.getElementById("employeeDepartment")
            .value.trim();

        if (!name || !department) {
            alert("Please enter employee name and department.");
            return;
        }

        try {
            // Send employee details to Flask
            const employeeId = document.getElementById("employeeId").value;

// If an ID exists, update the employee.
// Otherwise, create a new employee.
const isEditing = employeeId !== "";

const url = isEditing
    ? `${API_URL}/${employeeId}`
    : API_URL;

const response = await fetch(url, {
    method: isEditing ? "PUT" : "POST",
    headers: {
        "Content-Type": "application/json"
    },
    body: JSON.stringify({
        name: name,
        department: department
    })
});

            if (!response.ok) {
                throw new Error("Failed to add employee");
            }

            alert("Employee added successfully!");

            // Clear the form
            
// Clear the form after adding or updating
document.getElementById("employeeForm").reset();

// Clear the selected employee ID
document.getElementById("employeeId").value = "";

// Change the button back to Save Employee
document.getElementById("submitButton").textContent =
    "Save Employee";

// Refresh employee list
await loadEmployees();


        } catch (error) {
            console.error("Error:", error);
            alert("Unable to add employee.");
        }
    });
