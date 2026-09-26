import { useState } from "react";
import { useApp } from "../store.jsx";

const EMPTY_FORM = { fullName: "", email: "", phone: "", subject: "", preference: "email", message: "", newsletter: false };
const PREFERENCES = ["email", "phone", "sms"];
const SUBJECTS = ["order", "return", "technical", "other"];

export default function Contact() {
  const { showToast, t } = useApp();
  const [form, setForm] = useState(EMPTY_FORM);
  const [errors, setErrors] = useState([]);
  const [success, setSuccess] = useState(null);
  const [faqOpen, setFaqOpen] = useState(false);
  const [formKey, setFormKey] = useState(0); // remounts the form to clear the file input

  const setField = (name, value) => setForm(f => ({ ...f, [name]: value }));

  function resetForm() {
    setForm(EMPTY_FORM);
    setFormKey(k => k + 1);
  }

  function handleSubmit(e) {
    e.preventDefault();
    const found = [];
    if (!form.fullName.trim()) found.push("err.name");
    if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(form.email)) found.push("err.email");
    if (!form.subject) found.push("err.subject");
    if (form.message.trim().length < 10) found.push("err.message");
    setErrors(found);
    if (found.length) {
      setSuccess(null);
      return;
    }
    setSuccess(form.preference);
    resetForm();
    showToast(t("toast.messageSent"));
  }

  function handleClear() {
    resetForm();
    setErrors([]);
    setSuccess(null);
  }

  return (
    <>
      <h1 className="page-title" id="contact-title" data-testid="contact-page-title" data-qa="page-title">{t("contact.title")}</h1>

      <div className="contact-layout">
        <section className="card" id="contact-card" data-testid="contact-card" data-qa="contact-container">
          <div id="contact-success" className={"alert alert-success" + (success ? " visible" : "")} data-testid="contact-success-message" data-qa="contact-success" role="status">
            {success && t("contact.success", { channel: t(`channel.${success}`) })}
          </div>
          <div id="contact-error" className={"alert alert-error" + (errors.length ? " visible" : "")} data-testid="contact-error-message" data-qa="contact-error" role="alert">
            {errors.map(k => t(k)).join(" • ")}
          </div>

          <form key={formKey} onSubmit={handleSubmit} id="contact-form" name="contactForm" data-testid="contact-form" data-qa="contact-form" noValidate>
            <div className="form-row">
              <div className="form-group">
                <label className="form-label" htmlFor="contact-name">{t("contact.name")}</label>
                <input
                  type="text"
                  value={form.fullName}
                  onChange={e => setField("fullName", e.target.value)}
                  id="contact-name"
                  name="fullName"
                  className="form-input input-fullname"
                  data-testid="contact-name-input"
                  data-qa="full-name"
                  aria-label={t("contact.name")}
                  placeholder={t("contact.namePlaceholder")}
                  title={t("contact.name")}
                  autoComplete="name"
                />
              </div>
              <div className="form-group">
                <label className="form-label" htmlFor="contact-email">{t("contact.email")}</label>
                <input
                  type="email"
                  value={form.email}
                  onChange={e => setField("email", e.target.value)}
                  id="contact-email"
                  name="email"
                  className="form-input input-email"
                  data-testid="contact-email-input"
                  data-qa="email"
                  aria-label={t("contact.emailAria")}
                  placeholder="name@example.com"
                  title={t("contact.email")}
                  autoComplete="email"
                />
              </div>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label className="form-label" htmlFor="contact-phone">{t("contact.phone")}</label>
                <input
                  type="tel"
                  value={form.phone}
                  onChange={e => setField("phone", e.target.value)}
                  id="contact-phone"
                  name="phone"
                  className="form-input input-phone"
                  data-testid="contact-phone-input"
                  data-qa="phone"
                  aria-label={t("contact.phoneAria")}
                  placeholder="+90 5xx xxx xx xx"
                  title={t("contact.phone")}
                  autoComplete="tel"
                />
              </div>
              <div className="form-group">
                <label className="form-label" htmlFor="contact-subject">{t("contact.subject")}</label>
                <select
                  value={form.subject}
                  onChange={e => setField("subject", e.target.value)}
                  id="contact-subject"
                  name="subject"
                  className="form-select select-subject"
                  data-testid="contact-subject-select"
                  data-qa="subject"
                  aria-label={t("contact.subject")}
                  title={t("contact.subject")}
                >
                  <option value="">{t("contact.subjectSelect")}</option>
                  {SUBJECTS.map(s => <option key={s} value={s}>{t(`subject.${s}`)}</option>)}
                </select>
              </div>
            </div>

            <div className="form-group">
              <span className="form-label">{t("contact.preference")}</span>
              <div className="radio-group" role="radiogroup" aria-label={t("contact.preferenceAria")} data-testid="contact-preference-group" data-qa="contact-preference">
                {PREFERENCES.map(p => (
                  <label key={p} className="form-check" htmlFor={`pref-${p}`}>
                    <input
                      type="radio"
                      checked={form.preference === p}
                      onChange={() => setField("preference", p)}
                      id={`pref-${p}`}
                      name="preference"
                      value={p}
                      className="radio-pref"
                      data-testid={`contact-pref-${p}`}
                      data-qa={`pref-${p}`}
                      aria-label={t(`pref.${p}Aria`)}
                      title={t(`pref.${p}`)}
                    />{" "}
                    {t(`pref.${p}`)}
                  </label>
                ))}
              </div>
            </div>

            <div className="form-group">
              <label className="form-label" htmlFor="contact-message">{t("contact.message")}</label>
              <textarea
                value={form.message}
                onChange={e => setField("message", e.target.value)}
                id="contact-message"
                name="message"
                className="form-textarea input-message"
                data-testid="contact-message-input"
                data-qa="message"
                aria-label={t("contact.message")}
                placeholder={t("contact.messagePlaceholder")}
                title={t("contact.message")}
                maxLength={500}
              />
              <div id="char-counter" className="result-count" data-testid="contact-char-counter" data-qa="char-count">
                {form.message.length} / 500
              </div>
            </div>

            <div className="form-group">
              <label className="form-label" htmlFor="contact-attachment">{t("contact.attachment")}</label>
              <input
                type="file"
                id="contact-attachment"
                name="attachment"
                className="form-input input-file"
                data-testid="contact-attachment-input"
                data-qa="attachment"
                aria-label={t("contact.attachment")}
                title={t("contact.attachmentTitle")}
                accept=".png,.jpg,.pdf,.txt"
              />
            </div>

            <div className="form-group">
              <label className="form-check" htmlFor="newsletter">
                <input
                  type="checkbox"
                  checked={form.newsletter}
                  onChange={e => setField("newsletter", e.target.checked)}
                  id="newsletter"
                  name="newsletter"
                  className="checkbox-newsletter"
                  data-testid="contact-newsletter-checkbox"
                  data-qa="newsletter"
                  aria-label={t("contact.newsletterAria")}
                  title={t("contact.newsletterTitle")}
                />{" "}
                {t("contact.newsletter")}
              </label>
            </div>

            <div style={{ display: "flex", gap: 10 }}>
              <button
                type="submit"
                id="contact-submit"
                name="send"
                className="btn btn-primary btn-send"
                data-testid="contact-submit-button"
                data-qa="send-message"
                aria-label={t("contact.sendAria")}
                title={t("contact.send")}
              >
                {t("contact.send")}
              </button>
              <button
                type="button"
                onClick={handleClear}
                id="contact-clear"
                name="clear"
                className="btn btn-secondary btn-clear"
                data-testid="contact-clear-button"
                data-qa="clear-form"
                aria-label={t("contact.clearAria")}
                title={t("contact.clear")}
              >
                {t("contact.clear")}
              </button>
            </div>
          </form>
        </section>

        <aside className="card" id="contact-info" data-testid="contact-info" data-qa="contact-info-panel">
          <h3>{t("contact.infoTitle")}</h3>
          <ul className="info-list">
            <li>📍 {t("contact.address")}</li>
            <li>📞 0850 000 00 00</li>
            <li>✉️ support@shoplab.test</li>
            <li>🕘 {t("contact.hours")}</li>
          </ul>
          <button
            type="button"
            onClick={() => setFaqOpen(true)}
            id="faq-button"
            name="faq"
            className="btn btn-secondary btn-block"
            style={{ marginTop: 16 }}
            data-testid="faq-open-button"
            data-qa="open-faq"
            aria-label={t("contact.faq")}
            title={t("contact.faqTitle")}
          >
            {t("contact.faq")}
          </button>
        </aside>
      </div>

      <div
        id="faq-modal"
        className={"modal-backdrop" + (faqOpen ? " open" : "")}
        data-testid="faq-modal"
        data-qa="faq-dialog"
        role="dialog"
        aria-modal="true"
        aria-labelledby="faq-modal-title"
      >
        <div className="modal">
          <h3 id="faq-modal-title">{t("contact.faq")}</h3>
          <p><strong>{t("faq.q1")}</strong><br />{t("faq.a1")}</p>
          <p><strong>{t("faq.q2")}</strong><br />{t("faq.a2")}</p>
          <div className="modal-actions">
            <button
              type="button"
              onClick={() => setFaqOpen(false)}
              id="faq-close"
              className="btn btn-primary"
              data-testid="faq-close-button"
              data-qa="close-faq"
              aria-label={t("faq.close")}
              title={t("faq.close")}
            >
              {t("faq.close")}
            </button>
          </div>
        </div>
      </div>
    </>
  );
}
