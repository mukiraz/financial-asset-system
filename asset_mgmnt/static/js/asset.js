'use strict'

// DOMContentLoaded handler to initialize various parts of the interface
document.addEventListener('DOMContentLoaded', function () {
    initializeAlertFadeOut();
    handleModalEvents();
    applyValidationToForms();
    manipulateOptionsValues();
    disableFieldsBasedOnWelcomeText();
    handleAssetTypeChanges();
    installLineChart();
});

function installLineChart() {
    const categoryElement = document.getElementById('category_id_data');
    const categoryId = categoryElement.getAttribute('data-category-id');
    const currencyDropdownItems = document.querySelectorAll('#dropdownMenuButton1 ~ .dropdown-menu .dropdown-item');
    const timeDropdownItems = document.querySelectorAll('#dropdownMenuButton2 ~ .dropdown-menu .dropdown-item');
       
    let selectedCurrency = 1;
    let selectedTime = "daily";
    let endpoint = '';
    
    if (currencyDropdownItems.length == 0) {
        return;
    }

    let selectedCurrencyText = currencyDropdownItems[0].innerText;

    let selectedTimeText = timeDropdownItems[0].innerText;

    const graphParity = document.getElementById('graph_parity');
    const graphPeriod = document.getElementById('graph_period');


    currencyDropdownItems.forEach(item => {
        item.addEventListener('click', function () {
            selectedCurrency = this.getAttribute('data-currency-id');
            endpoint = `${origin}/asset/get_performance_line_data/${categoryId}/${selectedCurrency}/${selectedTime}/`;
            createLineChart(endpoint,'performanceLine');
            graphParity.innerText = this.innerText;
        });
    });

    timeDropdownItems.forEach(item => {
        item.addEventListener('click', function () {
            selectedTime = this.getAttribute('data-time-period');
            endpoint = `${origin}/asset/get_performance_line_data/${categoryId}/${selectedCurrency}/${selectedTime}/`;
            createLineChart(endpoint,'performanceLine');
            graphPeriod.innerText = this.innerText;
        });
    });

    endpoint = `${origin}/asset/get_performance_line_data/${categoryId}/${selectedCurrency}/${selectedTime}/`;
    graphParity.innerText = selectedCurrencyText;
    graphPeriod.innerText = selectedTimeText;

    createLineChart(endpoint,'performanceLine');
}

// Disable fields or hide warnings based on the first word in welcome text
function disableFieldsBasedOnWelcomeText() {
    const categoryData = document.getElementById('category_id_data');
    const isAutoUpdated = categoryData.getAttribute('data-is-auto-updated');
    const unitPrices = document.querySelectorAll('.unit-price');
    const cashUnits = document.querySelectorAll('.cash-unit');
    const cashWarnings = document.querySelectorAll('.cash-warning');
    const assetTypeControls = document.querySelectorAll('.asset-type-control');

    if (isAutoUpdated == 'False') {
        assetTypeControls.forEach((element) => {            
            element.style.setProperty('display', 'none', 'important');
        });
        unitPrices.forEach((unitPrice) => {
            unitPrice.setAttribute('value', 1)
            unitPrice.disabled = true
        });
        cashUnits.forEach((cashUnit) => {
            cashUnit.selectedIndex = 3
            cashUnit.setAttribute('value', 3)
            cashUnit.disabled = true
        });

        
    } else {
        assetTypeControls.forEach((element) => {            
            element.style.setProperty('display', '', 'important');
        });
        cashWarnings.forEach((cashWarning) => {
            cashWarning.style.display = 'none'
        });
        
    }
}

// Fade out alert after a specific time
function initializeAlertFadeOut() {
    const alertElement = document.getElementById('alert')
    if (alertElement) {
        setTimeout(() => {
            alertElement.style.transition = 'opacity 1s'
            alertElement.style.opacity = '0' // Fade out the alert
            setTimeout(() => {
                alertElement.style.display = 'none' // Hide the alert
            }, 500) // Adjust timing to match the transition duration
        }, 1500)
    }
}

// Handle modal related events for delete and update actions
function handleModalEvents() {
    const deleteAssetModal = document.getElementById('deleteAssetModal');
    const updateAssetModal = document.getElementById('updateAssetModal');

    if (deleteAssetModal) {
        deleteAssetModal.addEventListener('show.bs.modal', (event) => {
            setupDeleteModal(event)
        })
    }

    if (updateAssetModal) {
        updateAssetModal.addEventListener('show.bs.modal', (event) => {
            setupUpdateModal(event, 'update')
        })
    }

}

// Setup delete modal with dynamic content based on the triggered button
function setupDeleteModal(event) {
    const button = event.relatedTarget
    const object_id = button.getAttribute('data-asset-id').replace(',', '')
    const asset_type = button.getAttribute('data-asset-type')
    const deleteInput = document.getElementById('deleteinput')
    const deleteAlertMessage = document.getElementById('deletAlertHeader')

    deleteInput.value = object_id
    deleteAlertMessage.innerText = `${asset_type} varlığını silmek istediğinizden emin misiniz?`
}

// Setup update modal with values from the asset being updated
function setupUpdateModal(event, prefix) {
    const button = event.relatedTarget;
    const asset = {
        asset_type: button.getAttribute('data-asset-asset-type').replace('.', ''),
        buy_date: formatDate(button.getAttribute('data-asset-buy-date')),
        buy_unit_price: button.getAttribute('data-asset-buy-unit-price').replace('.', '').replace(',', '.'),
        number: button.getAttribute('data-asset-number').replace('.', '').replace(',', '.'),
        unit_type: button.getAttribute('data-asset-unit-type'),
        account: button.getAttribute('data-asset-account'),
        currency: button.getAttribute('data-asset-currency'),
        asset_id: button.getAttribute('data-asset-asset-id').replace('.', '')
    };
    // Format the date if it's not null or "None"
    if (asset.buy_date && asset.buy_date !== 'None') {
        asset.buy_date = formatDate(asset.buy_date);
    } else {
        asset.buy_date = '';
    }

    const fields = {
        asset_type: document.getElementById(`${prefix}_asset_asset_type`),
        buy_date: document.getElementById(`${prefix}_asset_buy_date`),
        buy_unit_price: document.getElementById(`${prefix}_asset_buy_unit_price`),
        number: document.getElementById(`${prefix}_asset_number`),
        unit_type: document.getElementById(`${prefix}_asset_unit_type`),
        account: document.getElementById(`${prefix}_asset_account`),
        currency: document.getElementById(`${prefix}_asset_currency`),
        asset_id: document.getElementById(`${prefix}_asset_id`)
    };

    Object.entries(asset).forEach(([key, value]) => {
        if (fields[key]) {            
            if (fields[key].tagName === 'SELECT') {
                const option = fields[key].querySelector(`option[value="${value}"]`);
                if (option) {
                    option.selected = true;
                } else {
                    console.error(`Option with value ${value} not found for ${key}`);
                }
            } else {
                fields[key].value = value;
            }
        } else {
            console.error(`Trying to set value for undefined element: ${key}`);
        }
    });
}

function formatDate(dateStr) {
    if (!dateStr || dateStr === 'None') return '';
    const date = new Date(dateStr);
    if (isNaN(date)) {
        const parsedDate = Date.parse(dateStr);
        if (!isNaN(parsedDate)) {
            return new Date(parsedDate).toISOString().split('T')[0];
        }
        console.error(`Invalid date string: ${dateStr}`);
        return '';
    }
    return date.toISOString().split('T')[0];
}
// Apply custom validation to forms
function applyValidationToForms() {
    const forms = document.querySelectorAll('.needs-validation')

    forms.forEach((form) => {
        form.addEventListener(
            'submit',
            (event) => {
                if (!form.checkValidity()) {
                    event.preventDefault()
                    event.stopPropagation()
                } else {
                    setCashValues()
                }
                form.classList.add('was-validated')
            },
            false
        )
    })
}

// Additional function to remove commas in option values
function manipulateOptionsValues() {
    const options = document.querySelectorAll('option')

    options.forEach((option) => {
        if (option.value.includes(',')) {
            option.value = option.value.replace(/,/g, '')
        }
    })
}


// Set cash values, used in form submission
function setCashValues() {
    const unitPrices = document.querySelectorAll('.unit-price')
    const cashUnits = document.querySelectorAll('.cash-unit')

    unitPrices.forEach((unitPrice) => {
        unitPrice.setAttribute('value', 1)
        unitPrice.disabled = false
    })
    cashUnits.forEach((cashUnit) => {
        cashUnit.selectedIndex = 3
        cashUnit.setAttribute('value', 3)
        cashUnit.disabled = false
    })
}

// Handle changes in asset type and update related fields
function handleAssetTypeChanges() {
    const assetTypeSelect = document.getElementById('upt_asset_type_asset_type');
    const currentPriceInput = document.getElementById('upt_current_price');
    const descriptionInput = document.getElementById('upt_description');
    const assetTypeIdInput = document.getElementById('asset_type_id');


    assetTypeSelect.addEventListener('change', () => {
        const selectedOption = assetTypeSelect.options[assetTypeSelect.selectedIndex]
        currentPriceInput.value = selectedOption.getAttribute('data-asset-type-current-price').replace('.', '').replace(',', '.');
        descriptionInput.value = selectedOption.getAttribute('data-asset-type-description').replace('None', '');
        assetTypeIdInput.value = selectedOption.getAttribute('data-asset-type-id').replace('.', '').replace(',', '.');
    })
}