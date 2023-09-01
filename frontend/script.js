// document.addEventListener("DOMContentLoaded", function () {
//     getClubs(); // Populate club selection when the page loads
// });

// async function getClubs() {
//     try {
//         // Replace user_id with the actual user ID
//         const user_id = "someUserID";
//         const url = `/v1/${user_id}/bag/clubs`;
//         const response = await fetch(url);

//         if (response.ok) {
//             const clubs = await response.json();
//             populateClubDropdown(clubs);
//         } else {
//             console.log("Error fetching clubs:", response.status, response.statusText);
//         }

//     } catch (error) {
//         console.error("Error fetching clubs:", error);
//     }
// }

// function populateClubDropdown(clubs) {
//     const select = document.getElementById("clubSelect");
//     clubs.forEach(club => {
//         const option = document.createElement("option");
//         let displayText = club.type;

//         if (club.identifier && club.identifier !== "None") {
//             displayText += ` (${club.identifier})`;
//         }

//         option.value = displayText;
//         option.textContent = displayText;
//         select.appendChild(option);
//     });
// }

function getLocation() {
    return new Promise((resolve, reject) => {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                position => resolve(position),
                error => reject(error)
            );
        } else {
            reject(new Error("Geolocation is not supported by this browser."));
        }
    });
}

async function getNextShotLocation() {
    if (!navigator.geolocation) {
        alert("Geolocation is not supported by your browser.");
        return;
    }

    navigator.geolocation.getCurrentPosition(async (position) => {
        const lat = position.coords.latitude;
        const lng = position.coords.longitude;

        // Log to console for debugging
        console.log(`Latitude: ${lat}, Longitude: ${lng}`);

        // Update latitude and longitude on the web page
        document.getElementById("latitude").textContent = lat;
        document.getElementById("longitude").textContent = lng;

        const data = {
            latitude: lat,
            longitude: lng,
            // club: club
        };

        console.log("Data to send:", data);

        // Send data to your Python backend
        // Replace round_id and hole_number with actual values
        // const round_id = "someRoundID";
        // const hole_number = 1;

        // const url = `/v1/rounds/${round_id}/hole/${hole_number}/add_shot`;
        // const response = await fetch(url, {
        //     method: "PUT",
        //     headers: {
        //         "Content-Type": "application/json"
        //     },
        //     body: JSON.stringify(data)
        // });

        // if (response.ok) {
        //     const jsonData = await response.json();
        //     console.log("Response data:", jsonData);
        // } else {
        //     console.log("Error:", response.status, response.statusText);
        // }
    }, (error) => {
        console.error("Error getting location:", error);
    });
}

