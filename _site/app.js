/*
 * FIX BUG 1 + BUG 5: Xoá dead code ngoài scope .then() (dòng 78-111 cũ)
 * - Vấn đề: code cũ truy cập biến `data` ngoài callback → ReferenceError crash
 * - Fix: giữ lại code trong .then(), thêm null-safety cho fields optional
 * - Rủi ro: không có, chỉ xoá code lỗi
 * - Test: mở index.html, kiểm tra console không có lỗi
 */
fetch("member.yml")
  .then(res => res.text())
  .then(text => {
    const data = jsyaml.load(text);

    const app = document.getElementById("app");

    // HEADER
    app.innerHTML += `
      <div class="header">
        <img src="${data.photo || ''}" alt="photo"/>
        <div>
          <h1>${data.name || ''}</h1>
          <p>${data.title || ''}</p>
          <p>${data.department || ''}</p>
          <p>Email: ${data.email || ''}</p>
          <p>
            <a href="${data.linkedin || '#'}">LinkedIn</a> |
            <a href="${data.github || '#'}">GitHub</a> |
            <a href="${data.schorlar || data.scholar || '#'}">Scholar</a>
          </p>
        </div>
      </div>
    `;

    // ABOUT
    app.innerHTML += `
      <h2>About</h2>
      <p>${data.about || ''}</p>
    `;

    // EDUCATION — kiểm tra null trước khi forEach
    let eduHTML = "<h2>Education</h2><ul>";
    if (Array.isArray(data.educations)) {
      data.educations.forEach(e => {
        eduHTML += `
          <li>
            <b>${e.degree || ''}</b> - ${e.field || ''}<br>
            ${e.institution || ''} (${e.year || ''})
          </li>
        `;
      });
    }
    eduHTML += "</ul>";
    app.innerHTML += eduHTML;

    // PUBLICATIONS
    /* FIX: publications có thể là URL string hoặc array, handle cả 2 */
    if (typeof data.publications === 'string' && data.publications) {
      app.innerHTML += `
        <h2>Publications</h2>
        <a href="${data.publications}">View Publications</a>
      `;
    } else if (Array.isArray(data.publications) && data.publications.length > 0) {
      let pubHTML = "<h2>Publications</h2><ul>";
      data.publications.forEach(p => {
        pubHTML += `<li>${p}</li>`;
      });
      pubHTML += "</ul>";
      app.innerHTML += pubHTML;
    }

    // AWARDS — kiểm tra null trước khi forEach
    if (Array.isArray(data.awards) && data.awards.length > 0) {
      let awardHTML = "<h2>Awards</h2><ul>";
      data.awards.forEach(a => {
        awardHTML += `<li>${a}</li>`;
      });
      awardHTML += "</ul>";
      app.innerHTML += awardHTML;
    }

    // SERVICES — kiểm tra null cho cả services, conferences, journals
    if (data.services) {
      let serviceHTML = "<h2>Services</h2>";

      if (Array.isArray(data.services.conferences) && data.services.conferences.length > 0) {
        serviceHTML += "<h3>Conferences</h3><ul>";
        data.services.conferences.forEach(c => {
          serviceHTML += `<li>${c}</li>`;
        });
        serviceHTML += "</ul>";
      }

      if (Array.isArray(data.services.journals) && data.services.journals.length > 0) {
        serviceHTML += "<h3>Journals</h3><ul>";
        data.services.journals.forEach(j => {
          serviceHTML += `<li>${j}</li>`;
        });
        serviceHTML += "</ul>";
      }

      /* FIX: một số member dùng services.activities thay vì conferences */
      if (Array.isArray(data.services.activities) && data.services.activities.length > 0) {
        serviceHTML += "<h3>Activities</h3><ul>";
        data.services.activities.forEach(a => {
          serviceHTML += `<li>${a}</li>`;
        });
        serviceHTML += "</ul>";
      }

      app.innerHTML += serviceHTML;
    }

  })
  .catch(err => {
    /* FIX BUG 9: không swallow exception, log rõ ràng */
    console.error("[app.js] Lỗi khi load/parse member.yml:", err);
  });