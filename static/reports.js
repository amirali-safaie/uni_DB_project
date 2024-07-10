// reports.js
document.addEventListener('DOMContentLoaded', async function() {
    const reportsContainer = document.getElementById('reports-container');

    try {
        const response = await fetch('/support/reports');
        const reports = await response.json();

        reports.forEach(report => {
            const reportElement = document.createElement('div');
            reportElement.className = 'report';
            reportElement.innerHTML = `
                <h3>Report ID: ${report.report_id}</h3>
                <p>Writer ID: ${report.writer_id}</p>
                <p>Moderator ID: ${report.moderator_id}</p>
                <p>Advertise ID: ${report.advertise_id}</p>
                <p>Note: ${report.note}</p>
                <p>Status: ${report.status}</p>
                <p>Type: ${report.type_name}</p>
            `;
            reportsContainer.appendChild(reportElement);
        });
    } catch (error) {
        reportsContainer.textContent = 'An error occurred while fetching reports';
    }
});
