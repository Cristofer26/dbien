document.addEventListener('DOMContentLoaded', function() {
    let formCount = document.querySelectorAll('#pasajero-forms-container .pasajero-form').length || 1; // Contar desde 1 debido al formulario inicial

    const updateClonedForm = (newForm, index) => {
        // Actualizar IDs y nombres en los campos del formulario clonado
        newForm.innerHTML = newForm.innerHTML.replace(/_0_/g, `_${index}_`).replace(/-0-/g, `-${index}-`);

        // Limpiar los valores de los campos de entrada
        newForm.querySelectorAll('input, select').forEach(input => {
            input.value = '';
        });

        // Eliminar la fila de encabezados (si existe)
        const headerRow = newForm.querySelector('tr:first-child');
        if (headerRow) {
            headerRow.remove();
        }

        // Eliminar la etiqueta de "Pasajero Responsable" si está presente
        const responsableLabel = newForm.querySelector('.responsable-label');
        if (responsableLabel) {
            responsableLabel.remove();
        }
    };

    const updateTotalForms = () => {
        const totalFormsInput = document.querySelector('#id_pasajeros-TOTAL_FORMS');
        totalFormsInput.value = formCount.toString();
    };

    document.getElementById('add-more').addEventListener('click', function() {
        // Clonar el formulario original
        let originalForm = document.querySelector('#primer-pasajero table');
        let newForm = originalForm.cloneNode(true);

        updateClonedForm(newForm, formCount);

        // Añadir el nuevo formulario en el contenedor adecuado
        document.querySelector('#pasajero-forms-container').appendChild(newForm);

        formCount++;
        updateTotalForms();
    });

    // El código para guardar pasajeros sigue igual
});