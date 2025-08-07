--- C:\projetos\omaum\docs\Formulário Aluno OmAum.js
+++ C:\projetos\omaum\docs\Formulário Aluno OmAum.js
@@ -0,0 +1,308 @@
+/**
+ * Class representing a Student Registration Form for OmAum.
+ * Classe que representa um Formulário de Registro de Aluno para OmAum.
+ */
+class FormularioRegistroAluno {
+  /**
+   * Create a student registration form.
+   * Cria um formulário de registro de aluno.
+   * @param {Object} options - Configuration options for the form.
+   * @param {string} options.title - Form title.
+   * @param {string} options.description - Form description.
+   * @param {boolean} options.collectEmail - Whether to collect respondent's email.
+   * @param {string} [options.confirmationMessage] - Custom confirmation message after submission.
+   * @param {string} [options.language='pt-BR'] - Form language.
+   * @throws {Error} If required options are missing or invalid.
+   */
+  constructor(options) {
+    this.validateOptions(options);
+    
+    this.title = options.title;
+    this.description = options.description;
+    this.collectEmail = options.collectEmail;
+    this.confirmationMessage = options.confirmationMessage || this.localize('defaultConfirmationMessage');
+    this.language = options.language || 'pt-BR';
+    this.form = null;
+    this.formResponses = new Map(); // For caching form responses
+    this.translations = this.getTranslations();
+  }
+
+  /**
+   * Validate the options provided to the constructor.
+   * Valida as opções fornecidas ao construtor.
+   * @param {Object} options - Options to validate.
+   * @throws {Error} If any required option is missing or invalid.
+   */
+  validateOptions(options) {
+    if (!options || typeof options !== 'object') {
+      throw new Error(this.localize('errorInvalidOptions'));
+    }
+
+    const requiredStringFields = ['title', 'description'];
+    for (const field of requiredStringFields) {
+      if (typeof options[field] !== 'string' || options[field].trim().length === 0) {
+        throw new Error(this.localize('errorInvalidField', field));
+      }
+    }
+
+    if (typeof options.collectEmail !== 'boolean') {
+      throw new Error(this.localize('errorInvalidCollectEmail'));
+    }
+
+    const optionalStringFields = ['confirmationMessage', 'language'];
+    for (const field of optionalStringFields) {
+      if (options[field] !== undefined && (typeof options[field] !== 'string' || options[field].trim().length === 0)) {
+        throw new Error(this.localize('errorInvalidOptionalField', field));
+      }
+    }
+  }
+
+  /**
+   * Create and display the form.
+   * Cria e exibe o formulário.
+   * @return {string} The URL of the created form.
+   */
+  displayForm() {
+    try {
+      this.form = this.createForm();
+      const formUrl = this.form.getPublishedUrl();
+      console.log(this.localize('logFormCreated', formUrl));
+      return formUrl;
+    } catch (error) {
+      console.error(this.localize('logErrorCreatingForm', error.toString()));
+      throw error;
+    }
+  }
+
+  /**
+   * Create the Google Form based on the provided options.
+   * Cria o Formulário Google com base nas opções fornecidas.
+   * @return {FormApp.Form} The created form.
+   */
+  createForm() {
+    const form = FormApp.create(this.title);
+    form.setDescription(this.description);
+    form.setCollectEmail(this.collectEmail);
+    form.setConfirmationMessage(this.confirmationMessage);
+    form.setLanguage(this.language);
+
+    this.addPersonalDataSection(form);
+    this.addAddressSection(form);
+    this.addEmergencyContactsSection(form);
+    this.addMedicalInformationSection(form);
+
+    return form;
+  }
+
+  /**
+   * Add the personal data section to the form.
+   * Adiciona a seção de dados pessoais ao formulário.
+   * @param {FormApp.Form} form - The form to add the section to.
+   */
+  addPersonalDataSection(form) {
+    const section = form.addPageBreakItem().setTitle(this.localize('titlePersonalData'));
+    section.setHelpText(this.localize('descriptionPersonalData'));
+
+    form.addTextItem().setTitle(this.localize('cpf')).setRequired(true);
+    form.addTextItem().setTitle(this.localize('fullName')).setRequired(true);
+    form.addDateItem().setTitle(this.localize('birthDate')).setRequired(true);
+    form.addTimeItem().setTitle(this.localize('birthTime')).setRequired(true);
+    form.addTextItem().setTitle(this.localize('email')).setRequired(true);
+
+    const genderItem = form.addMultipleChoiceItem();
+    genderItem.setTitle(this.localize('gender'))
+      .setChoiceValues([
+        this.localize('male'),
+        this.localize('female'),
+        this.localize('preferNotToSay')
+      ])
+      .setRequired(true);
+  }
+
+  /**
+   * Add the address section to the form.
+   * Adiciona a seção de endereço ao formulário.
+   * @param {FormApp.Form} form - The form to add the section to.
+   */
+  addAddressSection(form) {
+    const section = form.addPageBreakItem().setTitle(this.localize('titleAddress'));
+    section.setHelpText(this.localize('descriptionAddress'));
+
+    form.addTextItem().setTitle(this.localize('street')).setRequired(true);
+    form.addTextItem().setTitle(this.localize('number')).setRequired(true);
+    form.addTextItem().setTitle(this.localize('complement'));
+    form.addTextItem().setTitle(this.localize('neighborhood')).setRequired(true);
+    form.addTextItem().setTitle(this.localize('city')).setRequired(true);
+    form.addTextItem().setTitle(this.localize('state')).setRequired(true);
+    form.addTextItem().setTitle(this.localize('zipCode')).setRequired(true);
+  }
+
+  /**
+   * Add the emergency contacts section to the form.
+   * Adiciona a seção de contatos de emergência ao formulário.
+   * @param {FormApp.Form} form - The form to add the section to.
+   */
+  addEmergencyContactsSection(form) {
+    const section = form.addPageBreakItem().setTitle(this.localize('titleEmergencyContacts'));
+    section.setHelpText(this.localize('descriptionEmergencyContacts'));
+
+    for (let i = 1; i <= 2; i++) {
+      form.addTextItem().setTitle(this.localize('emergencyContactName', i)).setRequired(true);
+      form.addTextItem().setTitle(this.localize('emergencyContactPhone', i)).setRequired(true);
+      form.addTextItem().setTitle(this.localize('emergencyContactRelationship', i)).setRequired(true);
+    }
+  }
+
+  /**
+   * Add the medical information section to the form.
+   * Adiciona a seção de informações médicas ao formulário.
+   * @param {FormApp.Form} form - The form to add the section to.
+   */
+  addMedicalInformationSection(form) {
+    const section = form.addPageBreakItem().setTitle(this.localize('titleMedicalInformation'));
+    section.setHelpText(this.localize('descriptionMedicalInformation'));
+
+    form.addTextItem().setTitle(this.localize('bloodType')).setRequired(true);
+    form.addTextItem().setTitle(this.localize('allergies'));
+    form.addTextItem().setTitle(this.localize('medications'));
+    form.addParagraphTextItem().setTitle(this.localize('medicalConditions'));
+  }
+
+  /**
+   * Process form submission.
+   * Processa o envio do formulário.
+   * @param {Object} formData - The data submitted through the form.
+   * @return {Object} Processed form data.
+   * @throws {Error} If there's an error during form submission processing.
+   */
+  submitForm(formData) {
+    try {
+      this.validateFormData(formData);
+      const sanitizedData = this.sanitizeData(formData);
+      // Here you would typically save the data to a database or perform other actions
+      // Aqui você normalmente salvaria os dados em um banco de dados ou realizaria outras ações
+      console.log(this.localize('logFormSubmitted'));
+      return sanitizedData;
+    } catch (error) {
+      console.error(this.localize('logErrorSubmittingForm', error.toString()));
+      throw error;
+    }
+  }
+
+  /**
+   * Validate the submitted form data.
+   * Valida os dados enviados pelo formulário.
+   * @param {Object} data - The data to be validated.
+   * @throws {Error} If the data is invalid.
+   */
+  validateFormData(data) {
+    const requiredFields = ['cpf', 'fullName', 'birthDate', 'email'];
+    for (const field of requiredFields) {
+      if (!data[field]) {
+        throw new Error(this.localize('errorRequiredField', field));
+      }
+    }
+
+    if (!this.isValidEmail(data.email)) {
+      throw new Error(this.localize('errorInvalidEmail'));
+    }
+
+    // Add more specific validations as needed
+  }
+
+  /**
+   * Validate email format.
+   * Valida o formato do email.
+   * @param {string} email - The email to be validated.
+   * @return {boolean} True if the email is valid, false otherwise.
+   */
+  isValidEmail(email) {
+    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
+    return emailRegex.test(email);
+  }
+
+  /**
+   * Sanitize form data to prevent XSS and SQL injection.
+   * Sanitiza os dados do formulário para prevenir XSS e injeção SQL.
+   * @param {Object} data - The data to be sanitized.
+   * @return {Object} The sanitized data.
+   */
sanitizeData(data) {
  const sanitizedData = {};
  for (const [key, value] of Object.entries(data)) {
    sanitizedData[key] = typeof value === 'string' ? this.sanitizeString(value) : value;
  }
  return sanitizedData;
}