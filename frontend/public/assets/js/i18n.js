// Minimal client-side i18n with FR/AR/EN
(function(){
  const dictionaries = {
    fr: {
      langName: 'Français',
      // Titres / App
      login_title: "Connexion - Bureau de gestion d'Inflation",
      app_title: "Bureau de Gestion d'Inflation",
      // Nav
      nav_home: 'Accueil',
      nav_dashboard: 'Tableau de bord',
      nav_login: 'Connexion',
      nav_join: 'Rejoindre',
      nav_about: 'À propos',
      nav_contact: 'Contact',
      nav_forecast: 'Prévisions',
      nav_reports: 'Rapports',
      nav_recommendations: 'Recommandations',
      nav_causal: 'Analyse causale',
      nav_feedback: 'Feedback',
      nav_users: 'Utilisateurs',
      nav_quality: 'Qualité données',
      nav_alerts: 'Alertes régionales',
      // Login/Signup
      email_label: 'Adresse email',
      password_label: 'Mot de passe',
      role_select: 'Sélectionnez votre rôle',
      login_btn: 'Se connecter',
      no_account: "Vous n'avez pas de compte ?",
      create_account: 'Créer un compte',
      forgot_password: 'Mot de passe oublié ?',
      dashboard_title: 'Tableau de bord',
      logout: 'Déconnexion',
      signup_title: 'Demande d\'accès',
      signup_sub: "Remplissez ce formulaire pour rejoindre la plateforme",
      label_first_name: 'Prénom',
      label_last_name: 'Nom',
      label_terms: "J'accepte les",
      label_terms_tos: "conditions d'utilisation",
      label_terms_priv: 'politique de confidentialité',
      create_account_btn: 'Envoyer la demande',
      have_account: 'Vous avez déjà un compte ?',
      sign_in: 'Se connecter',
      // placeholders & help
      first_name_ph: 'Votre prénom',
      last_name_ph: 'Votre nom',
      email_ph: 'votre@email.com',
      password_ph: '••••••••',
      confirm_password_ph: '••••••••',
      pwd_strength: 'Force du mot de passe:',
      pwd_type: 'Tapez votre mot de passe',
      // Hero
      hero_login: 'Accéder à la plateforme',
      hero_join: 'Rejoindre'
    },
    en: {
      langName: 'English',
      // Titles / App
      login_title: 'Sign in - Inflation Management Office',
      app_title: 'Inflation Management Office',
      // Nav
      nav_home: 'Home',
      nav_dashboard: 'Dashboard',
      nav_login: 'Login',
      nav_join: 'Join Us',
      nav_about: 'About',
      nav_contact: 'Contact',
      nav_forecast: 'Forecasts',
      nav_reports: 'Reports',
      nav_recommendations: 'Recommendations',
      nav_causal: 'Causal analysis',
      nav_feedback: 'Feedback',
      nav_users: 'Users',
      nav_quality: 'Data quality',
      nav_alerts: 'Regional alerts',
      // Login/Signup
      email_label: 'Email address',
      password_label: 'Password',
      role_select: 'Select your role',
      login_btn: 'Sign in',
      no_account: "Don’t have an account?",
      create_account: 'Create account',
      forgot_password: 'Forgot password?',
      dashboard_title: 'Dashboard',
      logout: 'Sign out',
      signup_title: 'Access request',
      signup_sub: 'Fill this form to join the platform',
      label_first_name: 'First name',
      label_last_name: 'Last name',
      label_terms: 'I agree to the',
      label_terms_tos: 'Terms of service',
      label_terms_priv: 'Privacy policy',
      create_account_btn: 'Send request',
      have_account: 'Already have an account?',
      sign_in: 'Sign in',
      // placeholders & help
      first_name_ph: 'Your first name',
      last_name_ph: 'Your last name',
      email_ph: 'your@email.com',
      password_ph: '••••••••',
      confirm_password_ph: '••••••••',
      pwd_strength: 'Password strength:',
      pwd_type: 'Type your password',
      // Hero
      hero_login: 'Access the platform',
      hero_join: 'Join Us'
    },
    ar: {
      langName: 'العربية',
      // Titles / App
      login_title: 'تسجيل الدخول - مكتب إدارة التضخم',
      app_title: 'مكتب إدارة التضخم',
      // Nav
      nav_home: 'الرئيسية',
      nav_dashboard: 'لوحة التحكم',
      nav_login: 'تسجيل الدخول',
      nav_join: 'انضم إلينا',
      nav_about: 'من نحن',
      nav_contact: 'اتصل بنا',
      nav_forecast: 'التوقعات',
      nav_reports: 'التقارير',
      nav_recommendations: 'التوصيات',
      nav_causal: 'التحليل السببي',
      nav_feedback: 'التغذية الراجعة',
      nav_users: 'المستخدمون',
      nav_quality: 'جودة البيانات',
      nav_alerts: 'إنذارات إقليمية',
      // Login/Signup
      email_label: 'البريد الإلكتروني',
      password_label: 'كلمة المرور',
      role_select: 'اختر الدور',
      login_btn: 'تسجيل الدخول',
      no_account: 'لا تملك حسابًا؟',
      create_account: 'إنشاء حساب',
      forgot_password: 'نسيت كلمة المرور؟',
      dashboard_title: 'لوحة التحكم',
      logout: 'تسجيل الخروج',
      signup_title: 'طلب الوصول',
      signup_sub: 'يرجى ملء هذا النموذج للانضمام إلى المنصة',
      label_first_name: 'الاسم الأول',
      label_last_name: 'اسم العائلة',
      label_terms: 'أوافق على',
      label_terms_tos: 'شروط الاستخدام',
      label_terms_priv: 'سياسة الخصوصية',
      create_account_btn: 'إرسال الطلب',
      have_account: 'لديك حساب بالفعل؟',
      sign_in: 'تسجيل الدخول',
      // placeholders & help
      first_name_ph: 'الاسم الأول',
      last_name_ph: 'اسم العائلة',
      email_ph: 'your@email.com',
      password_ph: '••••••••',
      confirm_password_ph: '••••••••',
      pwd_strength: 'قوة كلمة المرور:',
      pwd_type: 'اكتب كلمة المرور',
      // Hero
      hero_login: 'الدخول إلى المنصة',
      hero_join: 'انضم إلينا'
    }
  };

  function getLang(){ return localStorage.getItem('lang') || 'fr'; }
  function setLang(lang){ localStorage.setItem('lang', lang); applyI18n(); }

  // Merge helper: shallow merge dictionaries[fr|en|ar] with extra[fr|en|ar]
  function merge(extra){
    if(!extra) return;
    ['fr','en','ar'].forEach(l=>{
      if(extra[l] && typeof extra[l] === 'object'){
        Object.assign(dictionaries[l], extra[l]);
      }
    });
  }

  function applyI18n(){
    const lang = getLang();
    const dict = dictionaries[lang] || dictionaries.fr;
    document.documentElement.dir = (lang==='ar') ? 'rtl' : 'ltr';
    document.querySelectorAll('[data-i18n]').forEach(el=>{
      const key = el.getAttribute('data-i18n');
      if(dict[key]) el.textContent = dict[key];
    });
    // placeholders / titles / values
    document.querySelectorAll('[data-i18n-placeholder]').forEach(el=>{
      const key = el.getAttribute('data-i18n-placeholder');
      if(dict[key]) el.setAttribute('placeholder', dict[key]);
    });
    document.querySelectorAll('[data-i18n-title]').forEach(el=>{
      const key = el.getAttribute('data-i18n-title');
      if(dict[key]) el.setAttribute('title', dict[key]);
    });
  }

  function renderSwitcher(container){
    if(!container) return;
    container.innerHTML = '';
    // Use Tailwind classes to mimic simple text buttons FR EN AR
    const wrapper = document.createElement('div');
    wrapper.className = 'flex items-center space-x-6';

    const langs = [
      { code:'fr', label:'FR' },
      { code:'en', label:'EN' },
      { code:'ar', label:'AR' },
    ];

    const current = getLang();
    langs.forEach(({code,label})=>{
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.textContent = label;
      btn.className = 'text-white/90 hover:text-white tracking-wide';
      if (code === current) {
        btn.className += ' underline font-semibold';
      }
      btn.style.background = 'transparent';
      btn.style.border = 'none';
      btn.style.outline = 'none';
      btn.addEventListener('click',()=> setLang(code));
      wrapper.appendChild(btn);
    });

    container.appendChild(wrapper);
  }

  // Auto-merge external payload if present (window.I18N_PAYLOAD or <script id="i18n-payload">)
  function tryAutoMerge(){
    if(window.I18N_PAYLOAD){
      merge(window.I18N_PAYLOAD);
      return;
    }
    const script = document.getElementById('i18n-payload');
    if(script && script.type === 'application/json'){
      try { merge(JSON.parse(script.textContent)); } catch(_){}
    }
  }

  window.I18N = { applyI18n, renderSwitcher, setLang, getLang, merge };

  document.addEventListener('DOMContentLoaded', function(){
    tryAutoMerge();
    applyI18n();
  });
})();


