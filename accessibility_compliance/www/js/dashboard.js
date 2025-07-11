// Accessibility Dashboard JavaScript

// Initialize dashboard
document.addEventListener('DOMContentLoaded', function() {
    loadDashboardData();
    initializeChart();
});

// Load dashboard statistics
function loadDashboardData() {
    frappe.call({
        method: 'accessibility_compliance.api.get_dashboard_stats',
        callback: function(r) {
            if (r.message) {
                updateDashboardStats(r.message);
                updateScanResults(r.message.recent_scans);
            }
        }
    });
}

// Update dashboard statistics
function updateDashboardStats(data) {
    document.getElementById('total-scans').textContent = data.total_scans || 0;
    document.getElementById('total-issues').textContent = data.total_issues || 0;
    document.getElementById('compliance-score').textContent = data.avg_compliance_score ? data.avg_compliance_score + '%' : 'N/A';
    document.getElementById('last-scan').textContent = data.last_scan ? formatDate(data.last_scan) : 'Never';
}

// Update scan results list
function updateScanResults(scans) {
    const container = document.getElementById('scan-results-list');
    
    if (!scans || scans.length === 0) {
        container.innerHTML = '<p>No scans found. <a href="#" onclick="startNewScan()">Start your first scan</a></p>';
        return;
    }
    
    container.innerHTML = scans.map(scan => `
        <div class="scan-item">
            <div class="scan-info">
                <h4>${scan.url || scan.name}</h4>
                <p>Scanned: ${formatDate(scan.scan_date)}</p>
            </div>
            <div class="scan-status">
                <span class="status-badge ${getStatusClass(scan.total_issues)}">
                    ${scan.total_issues || 0} issues
                </span>
                <span style="font-size: 0.8rem; color: #6c757d;">
                    ${scan.compliance_score || 0}% compliant
                </span>
            </div>
        </div>
    `).join('');
}

// Get status class based on issue count
function getStatusClass(issues) {
    if (issues === 0) return 'status-success';
    if (issues <= 5) return 'status-warning';
    return 'status-danger';
}

// Format date for display
function formatDate(dateString) {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

// Initialize compliance chart
function initializeChart() {
    const canvas = document.getElementById('compliance-chart');
    const ctx = canvas.getContext('2d');
    
    // Simple chart implementation (you can replace with Chart.js)
    frappe.call({
        method: 'accessibility_compliance.api.get_compliance_trends',
        callback: function(r) {
            if (r.message && r.message.length > 0) {
                drawComplianceChart(ctx, r.message);
            } else {
                drawNoDataChart(ctx);
            }
        }
    });
}

// Draw compliance trend chart
function drawComplianceChart(ctx, data) {
    const canvas = ctx.canvas;
    const width = canvas.width = canvas.offsetWidth;
    const height = canvas.height = 300;
    
    ctx.clearRect(0, 0, width, height);
    
    if (data.length === 0) {
        drawNoDataChart(ctx);
        return;
    }
    
    // Simple line chart
    const padding = 40;
    const chartWidth = width - (padding * 2);
    const chartHeight = height - (padding * 2);
    
    // Find max score for scaling
    const maxScore = Math.max(...data.map(d => d.score), 100);
    
    // Draw axes
    ctx.strokeStyle = '#e9ecef';
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(padding, padding);
    ctx.lineTo(padding, height - padding);
    ctx.lineTo(width - padding, height - padding);
    ctx.stroke();
    
    // Draw line
    if (data.length > 1) {
        ctx.strokeStyle = '#007bff';
        ctx.lineWidth = 3;
        ctx.beginPath();
        
        data.forEach((point, index) => {
            const x = padding + (index / (data.length - 1)) * chartWidth;
            const y = height - padding - (point.score / maxScore) * chartHeight;
            
            if (index === 0) {
                ctx.moveTo(x, y);
            } else {
                ctx.lineTo(x, y);
            }
        });
        
        ctx.stroke();
        
        // Draw points
        ctx.fillStyle = '#007bff';
        data.forEach((point, index) => {
            const x = padding + (index / (data.length - 1)) * chartWidth;
            const y = height - padding - (point.score / maxScore) * chartHeight;
            
            ctx.beginPath();
            ctx.arc(x, y, 4, 0, 2 * Math.PI);
            ctx.fill();
        });
    }
    
    // Add labels
    ctx.fillStyle = '#6c757d';
    ctx.font = '12px sans-serif';
    ctx.textAlign = 'center';
    
    data.forEach((point, index) => {
        const x = padding + (index / (data.length - 1)) * chartWidth;
        const label = new Date(point.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
        ctx.fillText(label, x, height - 10);
    });
}

// Draw "no data" message
function drawNoDataChart(ctx) {
    const canvas = ctx.canvas;
    const width = canvas.width = canvas.offsetWidth;
    const height = canvas.height = 300;
    
    ctx.clearRect(0, 0, width, height);
    ctx.fillStyle = '#6c757d';
    ctx.font = '16px sans-serif';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText('No compliance data available', width / 2, height / 2);
    ctx.fillText('Run some scans to see trends', width / 2, height / 2 + 25);
}

// Start new scan
function startNewScan() {
    frappe.new_doc('Accessibility Scan');
}

// Export report
function exportReport() {
    frappe.call({
        method: 'accessibility_compliance.api.export_compliance_report',
        callback: function(r) {
            if (r.message) {
                // Download the report
                const link = document.createElement('a');
                link.href = r.message.url;
                link.download = r.message.filename;
                link.click();
                
                frappe.show_alert({
                    message: 'Report exported successfully',
                    indicator: 'green'
                });
            }
        },
        error: function() {
            frappe.show_alert({
                message: 'Failed to export report',
                indicator: 'red'
            });
        }
    });
}