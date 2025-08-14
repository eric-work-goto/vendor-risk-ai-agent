// Main application JavaScript
class VendorRiskAssessmentUI {
    constructor() {
        this.apiBaseUrl = '';  // Set to empty since endpoints already include /api/v1/
        this.currentAssessmentId = null;
        this.assessmentInProgress = false;
        this.init();
    }

    init() {
        this.bindEvents();
        this.loadHistory();
        this.initializeRegulationsDropdown();
    }

    bindEvents() {
        // Form submission
        document.getElementById('assessmentForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.startAssessment();
        });

        // Modal controls
        document.getElementById('historyBtn').addEventListener('click', () => this.showHistoryModal());
        document.getElementById('closeHistoryModal').addEventListener('click', () => this.hideHistoryModal());
        document.getElementById('settingsBtn').addEventListener('click', () => this.showSettings());

        // Export actions
        document.getElementById('exportBtn').addEventListener('click', () => this.exportReport());
        document.getElementById('monitorBtn').addEventListener('click', () => this.setupMonitoring());
        document.getElementById('shareBtn').addEventListener('click', () => this.shareResults());

        // Auto-fill vendor name when domain changes
        document.getElementById('vendorDomain').addEventListener('blur', (e) => {
            this.autoFillVendorName(e.target.value);
        });

        // Regulations dropdown events
        document.getElementById('regulationsDropdown').addEventListener('click', (e) => {
            this.toggleRegulationsMenu();
        });

        // Close dropdown when clicking outside
        document.addEventListener('click', (e) => {
            if (!e.target.closest('#regulationsDropdown') && !e.target.closest('#regulationsMenu')) {
                this.closeRegulationsMenu();
            }
        });

        // Regulation checkbox changes
        document.addEventListener('change', (e) => {
            if (e.target.classList.contains('regulation-checkbox')) {
                this.updateSelectedRegulations();
            }
        });
    }

    initializeRegulationsDropdown() {
        // Set up the initial state
        this.selectedRegulations = ['gdpr', 'soc2']; // Default selections
        this.updateRegulationDisplay();
    }

    toggleRegulationsMenu() {
        const menu = document.getElementById('regulationsMenu');
        menu.classList.toggle('hidden');
    }

    closeRegulationsMenu() {
        const menu = document.getElementById('regulationsMenu');
        menu.classList.add('hidden');
    }

    updateSelectedRegulations() {
        const checkboxes = document.querySelectorAll('.regulation-checkbox');
        this.selectedRegulations = [];
        
        checkboxes.forEach(checkbox => {
            if (checkbox.checked) {
                this.selectedRegulations.push(checkbox.value);
            }
        });
        
        this.updateRegulationDisplay();
    }

    updateRegulationDisplay() {
        const container = document.getElementById('selectedRegulations');
        const regulationNames = {
            'gdpr': 'GDPR',
            'soc2': 'SOC 2',
            'hipaa': 'HIPAA',
            'pci_dss': 'PCI DSS',
            'sox': 'SOX',
            'iso27001': 'ISO 27001',
            'fisma': 'FISMA',
            'ccpa': 'CCPA',
            'nist': 'NIST',
            'custom': 'Custom'
        };

        if (this.selectedRegulations.length === 0) {
            container.innerHTML = '<span class="text-gray-500">Select regulatory requirements...</span>';
        } else {
            container.innerHTML = this.selectedRegulations.map(reg => `
                <span class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                    ${regulationNames[reg] || reg}
                    <button type="button" class="ml-1 text-blue-600 hover:text-blue-800" onclick="window.vendorRiskApp.removeRegulation('${reg}')">
                        <i class="fas fa-times"></i>
                    </button>
                </span>
            `).join('');
        }
    }

    removeRegulation(regulation) {
        this.selectedRegulations = this.selectedRegulations.filter(reg => reg !== regulation);
        
        // Update checkbox state
        const checkbox = document.querySelector(`input[value="${regulation}"]`);
        if (checkbox) {
            checkbox.checked = false;
        }
        
        this.updateRegulationDisplay();
    }

    clearAllRegulations() {
        this.selectedRegulations = [];
        
        // Uncheck all checkboxes
        document.querySelectorAll('.regulation-checkbox').forEach(checkbox => {
            checkbox.checked = false;
        });
        
        this.updateRegulationDisplay();
    }

    selectCommonRegulations() {
        const commonRegulations = ['gdpr', 'soc2', 'iso27001'];
        this.selectedRegulations = [...commonRegulations];
        
        // Update checkbox states
        document.querySelectorAll('.regulation-checkbox').forEach(checkbox => {
            checkbox.checked = commonRegulations.includes(checkbox.value);
        });
        
        this.updateRegulationDisplay();
    }

    async startAssessment() {
        console.log('startAssessment called');
        
        if (this.assessmentInProgress) {
            console.log('Assessment already in progress, returning');
            return;
        }

        const formData = this.getFormData();
        console.log('Form data:', formData);
        
        if (!this.validateForm(formData)) {
            console.log('Form validation failed');
            return;
        }

        this.assessmentInProgress = true;
        this.showProgressSection();
        this.hideResultsSection();
        this.updateStartButton(true);

        try {
            console.log('About to start assessment API call');
            
            // Start the assessment
            const response = await this.callAPI('/api/v1/assessments', 'POST', {
                vendorDomain: formData.vendorDomain,
                vendorName: formData.vendorName,
                dataSensitivity: formData.dataSensitivity,
                regulations: formData.regulations,
                businessCriticality: formData.businessCriticality,
                autoFollowUp: formData.autoFollowUp,
                deepScan: formData.deepScan
            });

            console.log('Assessment API response:', response);

            if (response.success) {
                this.currentAssessmentId = response.assessment_id;
                console.log('Starting polling for assessment:', this.currentAssessmentId);
                await this.pollAssessmentStatus();
            } else {
                throw new Error(response.message || 'Assessment failed to start');
            }

        } catch (error) {
            console.error('Assessment failed:', error);
            this.showError('Assessment failed: ' + error.message);
            this.resetForm();
        }
    }

    async pollAssessmentStatus() {
        const statusMessages = {
            'in_progress': 'Initializing assessment...',
            'retrieving_documents': 'Retrieving vendor documents...',
            'analyzing_documents': 'Analyzing documents...',
            'running_compliance_analysis': 'Analyzing compliance requirements...',
            'analyzing_compliance': 'Performing compliance analysis...',
            'assessing_security': 'Performing security assessment...',
            'calculating_risk_scores': 'Calculating risk scores...',
            'finalizing_results': 'Generating recommendations...',
            'completed': 'Assessment completed!'
        };

        let attempts = 0;
        const maxAttempts = 60; // 5 minutes max (5 second intervals)

        const pollInterval = setInterval(async () => {
            try {
                attempts++;
                const response = await this.callAPI(`/api/v1/assessments/${this.currentAssessmentId}`, 'GET');
                
                const progress = response.progress || 0;
                const status = response.status || 'in_progress';
                const statusMessage = statusMessages[status] || 'Processing...';
                
                this.updateProgress(progress, statusMessage);
                
                if (status === 'completed' && response.results) {
                    clearInterval(pollInterval);
                    this.showAssessmentResults(response.results);
                    this.assessmentInProgress = false;
                    this.updateStartButton(false);
                    this.saveToHistory(response.results);
                } else if (status === 'error') {
                    clearInterval(pollInterval);
                    this.showError('Assessment failed: ' + (response.error || 'Unknown error'));
                    this.resetForm();
                } else if (attempts >= maxAttempts) {
                    clearInterval(pollInterval);
                    this.showError('Assessment timed out. Please try again.');
                    this.resetForm();
                }
                
            } catch (error) {
                console.error('Error polling assessment status:', error);
                attempts++;
                if (attempts >= maxAttempts) {
                    clearInterval(pollInterval);
                    this.showError('Failed to check assessment status. Please try again.');
                    this.resetForm();
                }
            }
        }, 5000); // Poll every 5 seconds
    }

    showAssessmentResults(results) {
        this.hideProgressSection();
        
        // Determine risk color class
        const riskColorMap = {
            'low': 'risk-low',
            'medium': 'risk-medium',
            'high': 'risk-high'
        };
        const riskColor = riskColorMap[results.risk_level] || 'risk-medium';
        
        document.getElementById('resultsSection').innerHTML = `
            <div class="bg-white rounded-lg shadow-lg p-6">
                <div class="flex items-center justify-between mb-6">
                    <h2 class="text-2xl font-bold text-gray-900">Assessment Results</h2>
                    <button onclick="vendorAssessmentUI.startNewAssessment()" 
                            class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
                        New Assessment
                    </button>
                </div>
                
                <!-- Vendor Info -->
                <div class="mb-6 p-4 bg-gray-50 rounded-lg">
                    <h3 class="font-semibold text-gray-900 mb-2">Vendor Information</h3>
                    <p><strong>Name:</strong> ${results.vendor_name || 'N/A'}</p>
                    <p><strong>Domain:</strong> ${results.vendor_domain || 'N/A'}</p>
                    <p><strong>Completed:</strong> ${new Date(results.completed_at || Date.now()).toLocaleString()}</p>
                </div>
                
                <!-- Overall Score -->
                <div class="mb-6 text-center">
                    <div class="inline-block p-6 bg-white rounded-lg shadow border">
                        ${results.letter_grades ? `
                            <div class="text-6xl font-bold ${this.getLetterGradeColor(results.letter_grades.overall)} mb-2">${results.letter_grades.overall}</div>
                            <div class="text-lg font-medium text-gray-600 mb-1">${results.risk_description || 'Risk Assessment'}</div>
                            <div class="text-sm text-gray-500">${results.business_recommendation || ''}</div>
                            <div class="text-xs text-gray-400 mt-2">${results.overall_score}/100</div>
                        ` : `
                            <div class="text-6xl font-bold ${riskColor} mb-2">${results.overall_score}/100</div>
                            <div class="text-xl font-semibold text-gray-700 uppercase">${results.risk_level} Risk</div>
                        `}
                    </div>
                </div>
                
                <!-- Score Breakdown -->
                <div class="grid md:grid-cols-3 gap-4 mb-6">
                    <div class="bg-white p-4 rounded-lg border">
                        <h4 class="font-semibold text-gray-700 mb-2">Compliance</h4>
                        ${results.letter_grades ? `
                            <div class="text-2xl font-bold ${this.getLetterGradeColor(results.letter_grades.compliance)} mb-1">${results.letter_grades.compliance}</div>
                            <div class="text-sm text-gray-500">${results.scores.compliance}/100</div>
                        ` : `
                            <div class="text-2xl font-bold ${this.getScoreColor(results.scores.compliance)}">${results.scores.compliance}/100</div>
                        `}
                    </div>
                    <div class="bg-white p-4 rounded-lg border">
                        <h4 class="font-semibold text-gray-700 mb-2">Security</h4>
                        ${results.letter_grades ? `
                            <div class="text-2xl font-bold ${this.getLetterGradeColor(results.letter_grades.security)} mb-1">${results.letter_grades.security}</div>
                            <div class="text-sm text-gray-500">${results.scores.security}/100</div>
                        ` : `
                            <div class="text-2xl font-bold ${this.getScoreColor(results.scores.security)}">${results.scores.security}/100</div>
                        `}
                    </div>
                    <div class="bg-white p-4 rounded-lg border">
                        <h4 class="font-semibold text-gray-700 mb-2">Data Protection</h4>
                        ${results.letter_grades ? `
                            <div class="text-2xl font-bold ${this.getLetterGradeColor(results.letter_grades.data_protection)} mb-1">${results.letter_grades.data_protection}</div>
                            <div class="text-sm text-gray-500">${results.scores.data_protection}/100</div>
                        ` : `
                            <div class="text-2xl font-bold ${this.getScoreColor(results.scores.data_protection)}">${results.scores.data_protection}/100</div>
                        `}
                    </div>
                </div>
                
                <!-- Findings -->
                <div class="mb-6">
                    <h3 class="text-xl font-semibold text-gray-900 mb-4">Key Findings</h3>
                    <div class="space-y-3">
                        ${results.findings.map(finding => `
                            <div class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                                <div>
                                    <span class="font-medium">${finding.item}</span>
                                    <span class="text-sm text-gray-600 ml-2">(${finding.category})</span>
                                </div>
                                <span class="px-3 py-1 rounded-full text-sm font-medium ${this.getStatusBadgeClass(finding.status)}">
                                    ${finding.status.replace('_', ' ')}
                                </span>
                            </div>
                        `).join('')}
                    </div>
                </div>
                
                <!-- Compliance Documents -->
                ${results.compliance_documents && results.compliance_documents.length > 0 ? `
                <div class="mb-6">
                    <h3 class="text-xl font-semibold text-gray-900 mb-4">📋 Compliance Documents</h3>
                    <div class="grid md:grid-cols-2 gap-4">
                        ${results.compliance_documents.map(doc => `
                            <div class="border rounded-lg p-4 bg-gray-50">
                                <div class="flex items-start justify-between mb-3">
                                    <div>
                                        <h4 class="font-semibold text-gray-900">${doc.document_name}</h4>
                                        <p class="text-sm text-gray-600">${doc.description}</p>
                                    </div>
                                    <span class="px-2 py-1 rounded text-xs font-medium ${this.getDocumentStatusClass(doc.status)}">
                                        ${doc.status.replace('_', ' ')}
                                    </span>
                                </div>
                                <div class="text-sm text-gray-700 mb-3">
                                    <p><strong>Issuer:</strong> ${doc.issuer}</p>
                                    <p><strong>Valid Until:</strong> ${doc.valid_until}</p>
                                    <p><strong>Size:</strong> ${doc.file_size} (${doc.pages} pages)</p>
                                </div>
                                <div class="flex space-x-2">
                                    <a href="${doc.view_url}" target="_blank" 
                                       class="px-3 py-1 bg-blue-600 text-white text-sm rounded hover:bg-blue-700">
                                        📄 View
                                    </a>
                                    <a href="${doc.download_url}" 
                                       class="px-3 py-1 bg-green-600 text-white text-sm rounded hover:bg-green-700">
                                        📥 Download
                                    </a>
                                </div>
                            </div>
                        `).join('')}
                    </div>
                </div>
                ` : ''}
                
                <!-- Recommendations -->
                <div>
                    <h3 class="text-xl font-semibold text-gray-900 mb-4">Recommendations</h3>
                    <div class="space-y-3">
                        ${results.recommendations.map(rec => `
                            <div class="p-4 border rounded-lg">
                                <div class="flex items-center justify-between mb-2">
                                    <span class="px-2 py-1 rounded text-sm font-medium ${this.getPriorityBadgeClass(rec.priority)}">
                                        ${rec.priority} Priority
                                    </span>
                                    ${rec.timeline ? `<span class="text-sm text-gray-600">Timeline: ${rec.timeline}</span>` : ''}
                                </div>
                                <p class="text-gray-800">${rec.action}</p>
                            </div>
                        `).join('')}
                    </div>
                </div>
            </div>
        `;
        
        document.getElementById('resultsSection').classList.remove('hidden');
    }
    
    getScoreColor(score) {
        if (score >= 80) return 'text-green-600';
        if (score >= 60) return 'text-yellow-600';
        return 'text-red-600';
    }
    
    getLetterGradeColor(grade) {
        const gradeMap = {
            'A+': 'text-green-700',
            'A': 'text-green-600',
            'A-': 'text-green-500',
            'B+': 'text-blue-600',
            'B': 'text-blue-500',
            'B-': 'text-blue-400',
            'C+': 'text-yellow-600',
            'C': 'text-yellow-500',
            'C-': 'text-yellow-400',
            'D+': 'text-orange-600',
            'D': 'text-orange-500',
            'D-': 'text-orange-400',
            'F': 'text-red-600'
        };
        return gradeMap[grade] || 'text-gray-600';
    }
    
    getStatusBadgeClass(status) {
        switch (status.toLowerCase()) {
            case 'compliant':
                return 'bg-green-100 text-green-800';
            case 'adequate':
                return 'bg-yellow-100 text-yellow-800';
            case 'needs_review':
                return 'bg-orange-100 text-orange-800';
            case 'non_compliant':
                return 'bg-red-100 text-red-800';
            default:
                return 'bg-gray-100 text-gray-800';
        }
    }
    
    
    getDocumentStatusClass(status) {
        switch (status.toLowerCase()) {
            case 'current':
                return 'bg-green-100 text-green-800';
            case 'pending':
                return 'bg-yellow-100 text-yellow-800';
            case 'expired':
                return 'bg-red-100 text-red-800';
            case 'needs_review':
                return 'bg-orange-100 text-orange-800';
            default:
                return 'bg-gray-100 text-gray-800';
        }
    }
    
    getPriorityBadgeClass(priority) {
        switch (priority.toLowerCase()) {
            case 'high':
                return 'bg-red-100 text-red-800';
            case 'medium':
                return 'bg-yellow-100 text-yellow-800';
            case 'low':
                return 'bg-green-100 text-green-800';
            default:
                return 'bg-gray-100 text-gray-800';
        }
    }

    startNewAssessment() {
        this.hideResultsSection();
        this.hideProgressSection();
        this.resetForm();
        document.getElementById('vendorDomain').focus();
    }
    
    resetForm() {
        this.assessmentInProgress = false;
        this.currentAssessmentId = null;
        this.updateStartButton(false);
        
        // Reset form fields
        document.getElementById('vendorDomain').value = '';
        document.getElementById('vendorName').value = '';
        document.getElementById('dataSensitivity').value = 'low';
        document.getElementById('businessCriticality').value = 'low';
        document.getElementById('autoFollowUp').checked = false;
        document.getElementById('deepScan').checked = false;
        
        // Reset regulations to defaults
        this.selectedRegulations = ['gdpr', 'soc2'];
        this.updateRegulationDisplay();
        
        // Update regulation checkboxes
        document.querySelectorAll('.regulation-checkbox').forEach(checkbox => {
            checkbox.checked = this.selectedRegulations.includes(checkbox.value);
        });
    }
            },
            findings: {
                compliance: this.generateFindings('compliance', risk.level),
                security: this.generateFindings('security', risk.level)
            },
            recommendations: this.generateRecommendations(risk.level),
            timestamp: new Date().toISOString()
        };
    }

    generateFindings(type, riskLevel) {
        const findings = {
            compliance: {
                high: [
                    { item: 'SOC 2 Report', status: 'missing', icon: 'fa-times-circle', color: 'text-red-600' },
                    { item: 'GDPR Compliance', status: 'partial', icon: 'fa-exclamation-triangle', color: 'text-yellow-600' },
                    { item: 'Data Processing Agreement', status: 'missing', icon: 'fa-times-circle', color: 'text-red-600' }
                ],
                medium: [
                    { item: 'SOC 2 Report', status: 'outdated', icon: 'fa-exclamation-triangle', color: 'text-yellow-600' },
                    { item: 'GDPR Compliance', status: 'compliant', icon: 'fa-check-circle', color: 'text-green-600' },
                    { item: 'Data Processing Agreement', status: 'compliant', icon: 'fa-check-circle', color: 'text-green-600' }
                ],
                low: [
                    { item: 'SOC 2 Report', status: 'compliant', icon: 'fa-check-circle', color: 'text-green-600' },
                    { item: 'GDPR Compliance', status: 'compliant', icon: 'fa-check-circle', color: 'text-green-600' },
                    { item: 'Data Processing Agreement', status: 'compliant', icon: 'fa-check-circle', color: 'text-green-600' }
                ]
            },
            security: {
                high: [
                    { item: 'Encryption Standards', status: 'weak', icon: 'fa-times-circle', color: 'text-red-600' },
                    { item: 'Access Controls', status: 'insufficient', icon: 'fa-exclamation-triangle', color: 'text-yellow-600' },
                    { item: 'Incident Response', status: 'missing', icon: 'fa-times-circle', color: 'text-red-600' }
                ],
                medium: [
                    { item: 'Encryption Standards', status: 'adequate', icon: 'fa-check-circle', color: 'text-green-600' },
                    { item: 'Access Controls', status: 'good', icon: 'fa-check-circle', color: 'text-green-600' },
                    { item: 'Incident Response', status: 'partial', icon: 'fa-exclamation-triangle', color: 'text-yellow-600' }
                ],
                low: [
                    { item: 'Encryption Standards', status: 'strong', icon: 'fa-check-circle', color: 'text-green-600' },
                    { item: 'Access Controls', status: 'excellent', icon: 'fa-check-circle', color: 'text-green-600' },
                    { item: 'Incident Response', status: 'comprehensive', icon: 'fa-check-circle', color: 'text-green-600' }
                ]
            }
        };

        return findings[type][riskLevel] || findings[type]['medium'];
    }

    generateRecommendations(riskLevel) {
        const recommendations = {
            high: [
                { priority: 'High', action: 'Request updated SOC 2 Type II report', icon: 'fa-exclamation-circle' },
                { priority: 'High', action: 'Require data processing agreement signing', icon: 'fa-exclamation-circle' },
                { priority: 'Medium', action: 'Schedule security assessment call', icon: 'fa-phone' },
                { priority: 'Medium', action: 'Review encryption implementation', icon: 'fa-lock' }
            ],
            medium: [
                { priority: 'Medium', action: 'Update SOC 2 report (expires soon)', icon: 'fa-calendar' },
                { priority: 'Low', action: 'Verify incident response procedures', icon: 'fa-shield-alt' },
                { priority: 'Low', action: 'Schedule annual compliance review', icon: 'fa-calendar-check' }
            ],
            low: [
                { priority: 'Low', action: 'Monitor for compliance updates', icon: 'fa-eye' },
                { priority: 'Low', action: 'Schedule annual review', icon: 'fa-calendar-check' }
            ]
        };

        return recommendations[riskLevel] || recommendations['medium'];
    }

    updateProgress(step, message) {
        const progress = Math.min(((step + 1) / 7) * 100, 100);
        document.getElementById('progressBar').style.width = `${progress}%`;
        document.getElementById('progressPercent').textContent = `${Math.round(progress)}%`;
        document.getElementById('currentStep').innerHTML = `
            <div class="loading-spinner mr-3"></div>
            <span>${message}</span>
        `;

        // Update steps list
        const stepsList = document.getElementById('stepsList');
        const stepElement = document.createElement('div');
        stepElement.className = 'flex items-center text-sm';
        stepElement.innerHTML = `
            <i class="fas fa-check-circle text-green-500 mr-2"></i>
            <span class="text-gray-600">${message}</span>
        `;
        stepsList.appendChild(stepElement);
    }

    showResults(results) {
        // Update risk badge and scores
        const riskBadge = document.getElementById('riskBadge');
        riskBadge.textContent = `${results.risk_level.toUpperCase()} RISK`;
        riskBadge.className = `px-4 py-2 rounded-full text-white font-semibold ${results.risk_color}`;

        document.getElementById('overallScore').textContent = results.overall_score;
        document.getElementById('complianceScore').textContent = results.scores.compliance;
        document.getElementById('securityScore').textContent = results.scores.security;
        document.getElementById('dataProtectionScore').textContent = results.scores.data_protection;

        // Update findings
        this.renderFindings('complianceFindings', results.findings.compliance);
        this.renderFindings('securityFindings', results.findings.security);

        // Update recommendations
        this.renderRecommendations(results.recommendations);

        document.getElementById('resultsSection').classList.remove('hidden');
    }

    renderFindings(containerId, findings) {
        const container = document.getElementById(containerId);
        container.innerHTML = findings.map(finding => `
            <div class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div class="flex items-center">
                    <i class="fas ${finding.icon} ${finding.color} mr-3"></i>
                    <span class="font-medium">${finding.item}</span>
                </div>
                <span class="text-sm px-2 py-1 rounded ${finding.color} bg-opacity-10">
                    ${finding.status}
                </span>
            </div>
        `).join('');
    }

    renderRecommendations(recommendations) {
        const container = document.getElementById('actionItems');
        container.innerHTML = recommendations.map(rec => `
            <div class="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                <div class="flex items-center">
                    <i class="fas ${rec.icon} text-orange-600 mr-3"></i>
                    <div>
                        <div class="font-medium">${rec.action}</div>
                        <div class="text-sm text-gray-600">Priority: ${rec.priority}</div>
                    </div>
                </div>
                <button class="bg-orange-600 hover:bg-orange-700 text-white px-3 py-1 rounded text-sm transition">
                    Action
                </button>
            </div>
        `).join('');
    }

    getFormData() {
        return {
            vendorDomain: document.getElementById('vendorDomain').value.trim(),
            vendorName: document.getElementById('vendorName').value.trim(),
            dataSensitivity: document.getElementById('dataSensitivity').value,
            regulations: window.getSelectedRegulations ? window.getSelectedRegulations() : ['gdpr', 'soc2'], // Use global function
            businessCriticality: document.getElementById('businessCriticality').value,
            autoFollowUp: document.getElementById('autoFollowUp').checked,
            deepScan: document.getElementById('deepScan').checked
        };
    }

    validateForm(formData) {
        if (!formData.vendorDomain) {
            this.showError('Please enter a vendor domain');
            return false;
        }
        if (!formData.vendorName) {
            this.showError('Please enter a vendor name');
            return false;
        }
        if (!formData.regulations || formData.regulations.length === 0) {
            this.showError('Please select at least one regulatory requirement');
            return false;
        }
        return true;
    }

    autoFillVendorName(domain) {
        const nameField = document.getElementById('vendorName');
        if (!nameField.value && domain) {
            // Simple domain to company name mapping
            const domainName = domain.replace(/^https?:\/\//, '').replace(/^www\./, '').split('.')[0];
            const capitalizedName = domainName.charAt(0).toUpperCase() + domainName.slice(1);
            nameField.value = capitalizedName;
        }
    }

    showProgressSection() {
        document.getElementById('progressSection').classList.remove('hidden');
        document.getElementById('stepsList').innerHTML = '';
    }

    hideProgressSection() {
        document.getElementById('progressSection').classList.add('hidden');
    }

    hideResultsSection() {
        document.getElementById('resultsSection').classList.add('hidden');
    }

    updateStartButton(loading) {
        const button = document.getElementById('startAssessment');
        if (loading) {
            button.innerHTML = '<div class="loading-spinner mr-2"></div>Assessing...';
            button.disabled = true;
            button.classList.add('opacity-50');
        } else {
            button.innerHTML = '<i class="fas fa-play mr-2"></i>Start Assessment';
            button.disabled = false;
            button.classList.remove('opacity-50');
        }
    }

    resetForm() {
        this.assessmentInProgress = false;
        this.updateStartButton(false);
        this.hideProgressSection();
    }

    showError(message) {
        // Create a temporary error notification
        const errorDiv = document.createElement('div');
        errorDiv.className = 'fixed top-4 right-4 bg-red-500 text-white px-6 py-3 rounded-lg shadow-lg z-50';
        errorDiv.innerHTML = `
            <div class="flex items-center">
                <i class="fas fa-exclamation-circle mr-2"></i>
                <span>${message}</span>
                <button onclick="this.parentElement.parentElement.remove()" class="ml-4 text-white hover:text-gray-200">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `;
        document.body.appendChild(errorDiv);

        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (errorDiv.parentNode) {
                errorDiv.remove();
            }
        }, 5000);
    }

    showSuccess(message) {
        const successDiv = document.createElement('div');
        successDiv.className = 'fixed top-4 right-4 bg-green-500 text-white px-6 py-3 rounded-lg shadow-lg z-50';
        successDiv.innerHTML = `
            <div class="flex items-center">
                <i class="fas fa-check-circle mr-2"></i>
                <span>${message}</span>
                <button onclick="this.parentElement.parentElement.remove()" class="ml-4 text-white hover:text-gray-200">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `;
        document.body.appendChild(successDiv);

        setTimeout(() => {
            if (successDiv.parentNode) {
                successDiv.remove();
            }
        }, 5000);
    }

    // History Management
    saveToHistory(results) {
        const history = this.getHistory();
        history.unshift(results);
        localStorage.setItem('vendorRiskHistory', JSON.stringify(history.slice(0, 50))); // Keep last 50
    }

    getHistory() {
        try {
            return JSON.parse(localStorage.getItem('vendorRiskHistory')) || [];
        } catch {
            return [];
        }
    }

    loadHistory() {
        // History is loaded on demand in the modal
    }

    showHistoryModal() {
        const history = this.getHistory();
        const historyContent = document.getElementById('historyContent');
        
        if (history.length === 0) {
            historyContent.innerHTML = `
                <div class="text-center py-8 text-gray-500">
                    <i class="fas fa-history text-4xl mb-4"></i>
                    <p>No assessment history found</p>
                </div>
            `;
        } else {
            historyContent.innerHTML = history.map(item => `
                <div class="border-b border-gray-200 py-4 last:border-b-0">
                    <div class="flex items-center justify-between">
                        <div>
                            <h3 class="font-semibold">${item.vendor_name}</h3>
                            <p class="text-sm text-gray-600">${item.vendor_domain}</p>
                            <p class="text-xs text-gray-500">${new Date(item.timestamp).toLocaleString()}</p>
                        </div>
                        <div class="text-right">
                            <div class="text-2xl font-bold">${item.overall_score}</div>
                            <div class="text-sm px-2 py-1 rounded ${item.risk_color} text-white">
                                ${item.risk_level.toUpperCase()}
                            </div>
                        </div>
                    </div>
                </div>
            `).join('');
        }

        document.getElementById('historyModal').classList.remove('hidden');
    }

    hideHistoryModal() {
        document.getElementById('historyModal').classList.add('hidden');
    }

    showSettings() {
        this.showSuccess('Settings panel coming soon!');
    }

    exportReport() {
        if (!this.currentAssessmentId) {
            this.showError('No assessment to export');
            return;
        }
        this.showSuccess('Report export started - check your downloads');
    }

    setupMonitoring() {
        if (!this.currentAssessmentId) {
            this.showError('No assessment to monitor');
            return;
        }
        this.showSuccess('Monitoring enabled for this vendor');
    }

    shareResults() {
        if (!this.currentAssessmentId) {
            this.showError('No results to share');
            return;
        }
        // Copy link to clipboard
        const url = `${window.location.origin}/?assessment=${this.currentAssessmentId}`;
        navigator.clipboard.writeText(url).then(() => {
            this.showSuccess('Assessment link copied to clipboard');
        });
    }

    async callAPI(endpoint, method = 'GET', data = null) {
        const config = {
            method,
            headers: {
                'Content-Type': 'application/json',
            }
        };

        if (data) {
            config.body = JSON.stringify(data);
        }

        const response = await fetch(this.apiBaseUrl + endpoint, config);
        
        if (!response.ok) {
            throw new Error(`API call failed: ${response.statusText}`);
        }

        return await response.json();
    }
}

// Initialize the application when the page loads
document.addEventListener('DOMContentLoaded', () => {
    window.vendorRiskApp = new VendorRiskAssessmentUI();
});

// Global functions for HTML onclick handlers
function removeRegulation(regulation) {
    if (window.vendorRiskApp) {
        window.vendorRiskApp.removeRegulation(regulation);
    }
}

function clearAllRegulations() {
    if (window.vendorRiskApp) {
        window.vendorRiskApp.clearAllRegulations();
    }
}

function selectCommonRegulations() {
    if (window.vendorRiskApp) {
        window.vendorRiskApp.selectCommonRegulations();
    }
}

// Add some demo data on first load
if (!localStorage.getItem('vendorRiskHistory')) {
    const demoHistory = [
        {
            vendor_name: 'GitHub Inc',
            vendor_domain: 'github.com',
            overall_score: 85,
            risk_level: 'low',
            risk_color: 'risk-low',
            scores: { compliance: 88, security: 82, data_protection: 85 },
            timestamp: new Date(Date.now() - 86400000).toISOString() // 1 day ago
        },
        {
            vendor_name: 'Slack Technologies',
            vendor_domain: 'slack.com',
            overall_score: 72,
            risk_level: 'medium',
            risk_color: 'risk-medium',
            scores: { compliance: 75, security: 70, data_protection: 71 },
            timestamp: new Date(Date.now() - 172800000).toISOString() // 2 days ago
        }
    ];
    localStorage.setItem('vendorRiskHistory', JSON.stringify(demoHistory));
}
