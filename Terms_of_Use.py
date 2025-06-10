def run_terms_of_use(language_index):
    import time
    import streamlit as st
    import Background_Style
    global agree

    language_index = st.session_state.language_index

    translations_terms_of_use = {
        1: [
            "Welcome to our project", "Willkommen zu unserem Projekt", "Benvenuto nel nostro progetto",
            "Bienvenue dans notre projet", "Bienvenido a nuestro proyecto",
            "Bem-vindo ao nosso projeto", "Välkommen till vårt projekt", "Velkommen til vårt prosjekt",
            "Velkommen til vores projekt", "Witamy w naszym projekcie",
            "Добро пожаловать в наш проект", "Ласкаво просимо до нашого проекту"
        ],
        2: [
            "Disclaimer", "Haftungsausschluss", "Esclusione di responsabilità", "Avertissement", "Aviso legal",
            "Aviso de isenção de responsabilidade", "Ansvarsfriskrivning", "Ansvarsfraskrivelse", "Ansvarsfraskrivelse",
            "Zrzeczenie się odpowiedzialności",
            "Отказ от ответственности", "Застереження"
        ],
        3: [
            "This project is private and provided without any liability or warranty. The developer assumes no responsibility for damages or losses arising from the use of the software.",
            "Dieses Projekt ist privat und wird ohne jegliche Haftung oder Garantie bereitgestellt. Der Entwickler übernimmt keine Verantwortung für Schäden oder Verluste, die aus der Nutzung der Software entstehen können.",
            "Questo progetto è privato e fornito senza alcuna responsabilità o garanzia. Lo sviluppatore non si assume alcuna responsabilità per danni o perdite derivanti dall'uso del software.",
            "Ce projet est privé et fourni sans aucune responsabilité ni garantie. Le développeur n'assume aucune responsabilité pour les dommages ou pertes résultant de l'utilisation du logiciel.",
            "Este proyecto es privado y se proporciona sin ninguna responsabilidad o garantía. El desarrollador no asume ninguna responsabilidad por daños o pérdidas que surjan del uso del software.",
            "Este projeto é privado e fornecido sem qualquer responsabilidade ou garantia. O desenvolvedor não assume nenhuma responsabilidade por danos ou perdas decorrentes do uso do software.",
            "Detta projekt är privat och tillhandahålls utan ansvar eller garanti. Utvecklaren tar inget ansvar för skador eller förluster som uppstår vid användning av programvaran.",
            "Dette prosjektet er privat og leveres uten ansvar eller garanti. Utvikleren tar ikke ansvar for skader eller tap som oppstår ved bruk av programvaren.",
            "Dette projekt er privat og leveres uden ansvar eller garanti. Udvikleren påtager sig intet ansvar for skader eller tab, der opstår ved brug af softwaren.",
            "Ten projekt jest prywatny i udostępniany bez żadnej odpowiedzialności ani gwarancji. Twórca nie ponosi odpowiedzialności za szkody lub straty wynikłe z korzystania z oprogramowania.",
            "Этот проект является частным и предоставляется без какой-либо ответственности или гарантий. Разработчик не несет ответственности за ущерб или убытки, возникающие в результате использования программного обеспечения.",
            "Цей проект є приватним і надається без будь-якої відповідальності чи гарантій. Розробник не несе відповідальності за збитки чи втрати, що виникають внаслідок використання програмного забезпечення."
        ],
        4: [
            "Important notes:", "Wichtige Hinweise:", "Note importanti:", "Notes importantes:", "Notas importantes:",
            "Notas importantes:", "Viktiga noteringar:", "Viktige merknader:", "Vigtige noter:", "Ważne uwagi:",
            "Важные замечания:", "Важливі примітки:"
        ],
        5: [
            "No liability:", "Keine Haftung:", "Nessuna responsabilità:", "Aucune responsabilité:",
            "Sin responsabilidad:",
            "Sem responsabilidade:", "Inget ansvar:", "Ingen ansvar:", "Ingen ansvar:", "Brak odpowiedzialności:",
            "Отказ от ответственности:", "Жодної відповідальності:"
        ],
        6: [
            "Any liability of the developer, whether for direct or indirect damages, is excluded.",
            "Jegliche Haftung des Entwicklers, sei es für direkte oder indirekte Schäden, ist ausgeschlossen.",
            "Qualsiasi responsabilità dello sviluppatore, sia per danni diretti che indiretti, è esclusa.",
            "Toute responsabilité du développeur, qu'elle soit directe ou indirecte, est exclue.",
            "Cualquier responsabilidad del desarrollador, ya sea por daños directos o indirectos, está excluida.",
            "Qualquer responsabilidade do desenvolvedor, seja por danos diretos ou indiretos, está excluída.",
            "Allt ansvar från utvecklaren, oavsett om det är för direkta eller indirekta skador, är uteslutet.",
            "Ethvert ansvar fra utvikleren, enten det er for direkte eller indirekte skader, er utelukket.",
            "Ethvert ansvar fra udvikleren, hvad enten det er for direkte eller indirekte skader, er udelukket.",
            "Wszelka odpowiedzialność twórcy, zarówno za bezpośrednie, jak i pośrednie szkody, jest wyłączona.",
            "Любая ответственность разработчика, будь то за прямой или косвенный ущерб, исключается.",
            "Будь-яка відповідальність розробника, чи то за прямі, чи то за непрямі збитки, виключається."
        ],
        7: [
            "No warranty:", "Keine Garantie:", "Nessuna garanzia:", "Aucune garantie:", "Sin garantía:",
            "Sem garantia:", "Ingen garanti:", "Ingen garanti:", "Ingen garanti:", "Brak gwarancji:",
            "Без гарантии:", "Жодної гарантії:"
        ],
        8: [
            "No guarantee is given for the functionality, error-free operation, or security of the software.",
            "Es wird keine Garantie für die Funktionsweise, Fehlerfreiheit oder Sicherheit der Software gegeben.",
            "Non viene data alcuna garanzia per il funzionamento, l'assenza di errori o la sicurezza del software.",
            "Aucune garantie n'est donnée quant à la fonctionnalité, le fonctionnement sans erreur ou la sécurité du logiciel.",
            "No se da ninguna garantía sobre la funcionalidad, el funcionamiento sin errores o la seguridad del software.",
            "Não é dada nenhuma garantia quanto à funcionalidade, operação sem erros ou segurança do software.",
            "Ingen garanti ges för funktionaliteten, felfri drift eller säkerhet i programvaran.",
            "Ingen garanti gis for funksjonaliteten, feilfri drift eller sikkerhet til programvaren.",
            "Ingen garanti gives for funktionaliteten, fejlfri drift eller sikkerhed af softwaren.",
            "Nie udziela się żadnej gwarancji na funkcjonalność, bezbłędne działanie ani bezpieczeństwo oprogramowania.",
            "Не предоставляется никаких гарантий относительно функциональности, безошибочной работы или безопасности программного обеспечения.",
            "Жодних гарантій щодо функціональності, безпомилкової роботи чи безпеки програмного забезпечення не надається."
        ],
        9: [
            "No claims for damages:", "Keine Schadensersatzansprüche:", "Nessuna pretesa di risarcimento danni:",
            "Aucune réclamation pour dommages :",
            "Sin reclamaciones de daños:", "Sem reivindicações de danos:", "Inga krav på skadestånd:",
            "Ingen krav om erstatning:",
            "Ingen krav om erstatning:", "Brak roszczeń o odszkodowanie:", "Никаких претензий по возмещению убытков:",
            "Жодних претензій на відшкодування збитків:"
        ],
        10: [
            "Claims for damages are excluded.", "Ansprüche auf Schadensersatz sind ausgeschlossen.",
            "Le richieste di risarcimento danni sono escluse.",
            "Les réclamations pour dommages sont exclues.", "Las reclamaciones por daños quedan excluidas.",
            "As reivindicações por danos estão excluídas.",
            "Krav på skadestånd är uteslutna.", "Krav om erstatning er utelukket.", "Krav om erstatning er udelukket.",
            "Roszczenia odszkodowawcze są wyłączone.",
            "Претензии по возмещению убытков исключены.", "Претензії на відшкодування збитків виключаються."
        ],
        11: [
            "Use at your own risk:", "Nutzung auf eigene Gefahr:", "Uso a proprio rischio:",
            "Utilisation à vos risques et périls:", "Uso bajo su propio riesgo:",
            "Uso por sua conta e risco:", "Användning på egen risk:", "Bruk på eget ansvar:", "Brug på eget ansvar:",
            "Użytkowanie na własne ryzyko:",
            "Использование на свой страх и риск:", "Використання на власний ризик:"
        ],
        12: [
            "The use of the software is entirely at your own risk. You are responsible for taking all necessary measures to minimize potential risks.",
            "Die Nutzung der Software erfolgt vollständig auf eigene Gefahr. Der Nutzer ist selbst dafür verantwortlich, alle erforderlichen Maßnahmen zu treffen, um mögliche Risiken zu minimieren.",
            "L'uso del software è interamente a proprio rischio. Sei responsabile di adottare tutte le misure necessarie per ridurre al minimo i potenziali rischi.",
            "L'utilisation du logiciel se fait entièrement à vos risques et périls. Vous êtes responsable de prendre toutes les mesures nécessaires pour minimiser les risques potentiels.",
            "El uso del software es completamente bajo su propio riesgo. Usted es responsable de tomar todas las medidas necesarias para minimizar los posibles riesgos.",
            "O uso do software é inteiramente por sua conta e risco. Você é responsável por tomar todas as medidas necessárias para minimizar os riscos potenciais.",
            "Användningen av programvaran sker helt på egen risk. Du är ansvarig för att vidta alla nödvändiga åtgärder för att minimera potentiella risker.",
            "Bruk av programvaren er helt på eget ansvar. Du er ansvarlig for å ta alle nødvendige tiltak for å minimere potensielle risikoer.",
            "Brugen af softwaren sker helt på eget ansvar. Du er ansvarlig for at tage alle nødvendige foranstaltninger for at minimere potentielle risici.",
            "Korzystanie z oprogramowania odbywa się całkowicie na własne ryzyko. Jesteś odpowiedzialny za podjęcie wszelkich niezbędnych środków w celu zminimalizowania potencjalnych ryzyk.",
            "Использование программного обеспечения осуществляется полностью на ваш страх и риск. Вы несете ответственность за принятие всех необходимых мер для минимизации потенциальных рисков.",
            "Використання програмного забезпечення здійснюється повністю на ваш власний ризик. Ви несете відповідальність за вжиття всіх необхідних заходів для мінімізації потенційних ризиків."
        ],
        13: [
            "No warranty:", "Keine Gewährleistung:", "Nessuna garanzia:", "Aucune garantie:", "Sin garantía:",
            "Sem garantia:", "Ingen garanti:", "Ingen garanti:", "Ingen garanti:", "Brak gwarancji:",
            "Без гарантии:", "Жодної гарантії:"
        ],
        14: [
            "No warranty, either express or implied, is provided regarding merchantability, fitness for a particular purpose, or non-infringement of third-party rights.",
            "Es wird keine Gewährleistung, weder ausdrücklich noch stillschweigend, hinsichtlich der Marktfähigkeit, Eignung für einen bestimmten Zweck oder der Nichtverletzung von Rechten Dritter übernommen.",
            "Non viene fornita alcuna garanzia, esplicita o implicita, per quanto riguarda la commerciabilità, l'idoneità per un particolare scopo o la non violazione dei diritti di terzi.",
            "Aucune garantie, expresse ou implicite, n'est fournie concernant la qualité marchande, l'adéquation à un usage particulier ou le respect des droits des tiers.",
            "No se proporciona ninguna garantía, ya sea expresa o implícita, con respecto a la comerciabilidad, la idoneidad para un propósito particular o la no infracción de los derechos de terceros.",
            "Não é dada nenhuma garantia, seja expressa ou implícita, em relação à comercialização, adequação para um propósito específico ou não violação de direitos de terceiros.",
            "Ingen garanti, varken uttrycklig eller underförstådd, ges för säljbarhet, lämplighet för ett visst ändamål eller att inga tredje parts rättigheter kränks.",
            "Ingen garanti, verken uttrykt eller underforstått, gis for salgbarhet, egnethet for et bestemt formål eller ikke-krenkelse av tredjeparts rettigheter.",
            "Ingen garanti, hverken udtrykkelig eller stiltiende, gives vedrørende salgbarhed, egnethed til et bestemt formål eller ikke-krænkelse af tredjeparts rettigheder.",
            "Nie udziela się żadnej gwarancji, ani wyraźnej, ani dorozumianej, co do przydatności handlowej, przydatności do określonego celu lub nienaruszalności praw osób trzecich.",
            "Никаких гарантий, явных или подразумеваемых, относительно товарной пригодности, соответствия для конкретной цели или ненарушения прав третьих лиц не предоставляется.",
            "Жодних гарантій, явних чи неявних, щодо придатності для продажу, відповідності певній меті чи відсутності порушення прав третіх осіб не надається."
        ],
        15: [
            "Updates and support:", "Updates und Support:", "Aggiornamenti e supporto:", "Mises à jour et support:",
            "Actualizaciones y soporte:",
            "Atualizações e suporte:", "Uppdateringar och support:", "Oppdateringer og support:",
            "Opdateringer og support:", "Aktualizacje i wsparcie:",
            "Обновления и поддержка:", "Оновлення та підтримка:"
        ],
        16: [
            "There is no obligation to provide updates, patches, or support services. The developer reserves the right to change or discontinue the software at any time without notice.",
            "Es besteht keine Verpflichtung zur Bereitstellung von Updates, Patches oder Supportleistungen. Der Entwickler behält sich das Recht vor, die Software jederzeit und ohne Vorankündigung zu ändern oder einzustellen.",
            "Non vi è alcun obbligo di fornire aggiornamenti, patch o servizi di supporto. Lo sviluppatore si riserva il diritto di modificare o interrompere il software in qualsiasi momento senza preavviso.",
            "Il n'y a aucune obligation de fournir des mises à jour, des correctifs ou des services de support. Le développeur se réserve le droit de modifier ou d'arrêter le logiciel à tout moment sans préavis.",
            "No existe ninguna obligación de proporcionar actualizaciones, parches o servicios de soporte. El desarrollador se reserva el derecho de cambiar o descontinuar el software en cualquier momento sin previo aviso.",
            "Não há obrigação de fornecer atualizações, patches ou serviços de suporte. O desenvolvedor reserva-se o direito de alterar ou descontinuar o software a qualquer momento, sem aviso prévio.",
            "Det finns ingen skyldighet att tillhandahålla uppdateringar, patchar eller supporttjänster. Utvecklaren förbehåller sig rätten att ändra eller avbryta programvaran när som helst utan förvarning.",
            "Det er ingen forpliktelse til å tilby oppdateringer, oppdateringer eller støttetjenester. Utvikleren forbeholder seg retten til å endre eller avslutte programvaren når som helst uten varsel.",
            "Der er ingen forpligtelse til at levere opdateringer, rettelser eller supporttjenester. Udvikleren forbeholder sig retten til at ændre eller afbryde softwaren til enhver tid uden varsel.",
            "Nie ma obowiązku dostarczania aktualizacji, poprawek ani usług wsparcia. Twórca zastrzega sobie prawo do zmiany lub zaprzestania dostarczania oprogramowania w dowolnym momencie bez powiadomienia.",
            "Отсутствует обязательство предоставлять обновления, исправления или услуги поддержки. Разработчик оставляет за собой право изменять или прекращать использование программного обеспечения в любое время без предварительного уведомления.",
            "Відсутній обов'язок надавати оновлення, виправлення або послуги підтримки. Розробник залишає за собою право змінювати або припиняти роботу програмного забезпечення в будь-який час без попередження."
        ],
        17: [
            "External resources:", "Externe Ressourcen:", "Risorse esterne:", "Ressources externes:",
            "Recursos externos:",
            "Recursos externos:", "Externa resurser:", "Eksterne ressurser:", "Eksterne ressourcer:",
            "Zasoby zewnętrzne:",
            "Внешние ресурсы:", "Зовнішні ресурси:"
        ],
        18: [
            "If the software accesses external resources or third-party software, no responsibility is assumed for their availability, functionality, or security.",
            "Falls die Software auf externe Ressourcen oder Drittanbietersoftware zugreift, wird keine Verantwortung für deren Verfügbarkeit, Funktionalität oder Sicherheit übernommen.",
            "Se il software accede a risorse esterne o software di terze parti, non viene assunta alcuna responsabilità per la loro disponibilità, funzionalità o sicurezza.",
            "Si le logiciel accède à des ressources externes ou à des logiciels tiers, aucune responsabilité n'est assumée quant à leur disponibilité, fonctionnalité ou sécurité.",
            "Si el software accede a recursos externos o software de terceros, no se asume ninguna responsabilidad por su disponibilidad, funcionalidad o seguridad.",
            "Se o software acessar recursos externos ou software de terceiros, nenhuma responsabilidade é assumida por sua disponibilidade, funcionalidade ou segurança.",
            "Om programvaran får tillgång till externa resurser eller tredjepartsprogramvara, antas inget ansvar för deras tillgänglighet, funktionalitet eller säkerhet.",
            "Hvis programvaren får tilgang til eksterne ressurser eller tredjeparts programvare, påtas det intet ansvar for tilgjengelighet, funksjonalitet eller sikkerhet.",
            "Hvis softwaren får adgang til eksterne ressourcer eller tredjeparts software, påtages der intet ansvar for tilgængelighed, funktionalitet eller sikkerhed.",
            "Jeśli oprogramowanie uzyskuje dostęp do zasobów zewnętrznych lub oprogramowania innych firm, nie ponosi się odpowiedzialności za ich dostępność, funkcjonalność lub bezpieczeństwo.",
            "Если программное обеспечение получает доступ к внешним ресурсам или программному обеспечению сторонних производителей, никакая ответственность за их доступность, функциональность или безопасность не принимается.",
            "Якщо програмне забезпечення отримує доступ до зовнішніх ресурсів або програмного забезпечення сторонніх розробників, жодна відповідальність за їх доступність, функціональність чи безпеку не покладається."
        ],
        19: [
            "Data security:", "Datensicherheit:", "Sicurezza dei dati:", "Sécurité des données:", "Seguridad de datos:",
            "Segurança de dados:", "Datasäkerhet:", "Datasikkerhet:", "Datasikkerhed:", "Bezpieczeństwo danych:",
            "Безопасность данных:", "Безпека даних:"
        ],
        20: [
            "No responsibility is assumed for the security of data processed or stored by the software. Users should ensure they have appropriate security measures.",
            "Es wird keine Verantwortung für die Sicherheit der durch die Software verarbeiteten oder gespeicherten Daten übernommen. Nutzer sollten sicherstellen, dass sie über angemessene Sicherheitsmaßnahmen verfügen.",
            "Non viene assunta alcuna responsabilità per la sicurezza dei dati elaborati o memorizzati dal software. Gli utenti dovrebbero assicurarsi di disporre di misure di sicurezza appropriate.",
            "Aucune responsabilité n'est assumée pour la sécurité des données traitées ou stockées par le logiciel. Les utilisateurs doivent s'assurer qu'ils disposent de mesures de sécurité appropriées.",
            "No se asume ninguna responsabilidad por la seguridad de los datos procesados o almacenados por el software. Los usuarios deben asegurarse de tener medidas de seguridad adecuadas.",
            "Não é assumida nenhuma responsabilidade pela segurança dos dados processados ou armazenados pelo software. Os usuários devem garantir que possuem medidas de segurança apropriadas.",
            "Ingen ansvar tas för säkerheten för data som behandlas eller lagras av programvaran. Användare bör säkerställa att de har lämpliga säkerhetsåtgärder.",
            "Ingen ansvar tas for sikkerheten til data som behandles eller lagres av programvaren. Brukere bør sørge for at de har passende sikkerhetstiltak.",
            "Der tages intet ansvar for sikkerheden af data, der behandles eller opbevares af softwaren. Brugere skal sikre, at de har passende sikkerhedsforanstaltninger.",
            "Nie ponosi się odpowiedzialności za bezpieczeństwo danych przetwarzanych lub przechowywanych przez oprogramowanie. Użytkownicy powinni upewnić się, że mają odpowiednie środki bezpieczeństwa.",
            "Никакая ответственность за безопасность данных, обрабатываемых или хранимых программным обеспечением, не принимается. Пользователи должны обеспечить наличие соответствующих мер безопасности.",
            "Жодна відповідальність за безпеку даних, оброблених або збережених програмним забезпеченням, не покладається. Користувачі повинні переконатися, що мають відповідні заходи безпеки."
        ],
        21: [
            "Illegal use:", "Rechtswidrige Nutzung:", "Uso illegale:", "Usage illégal:", "Uso ilegal:",
            "Uso ilegal:", "Olaglig användning:", "Ulovlig bruk:", "Ulovlig bruk:", "Nielegalne użycie:",
            "Незаконное использование:", "Незаконне використання:"
        ],
        22: [
            "The user is responsible for ensuring that the use of the software does not violate applicable laws or regulations.",
            "Der Nutzer ist dafür verantwortlich, sicherzustellen, dass die Nutzung der Software nicht gegen geltende Gesetze oder Vorschriften verstößt.",
            "L'utente è responsabile di assicurarsi che l'uso del software non violi le leggi o i regolamenti applicabili.",
            "L'utilisateur est responsable de s'assurer que l'utilisation du logiciel ne viole pas les lois ou réglementations applicables.",
            "El usuario es responsable de asegurarse de que el uso del software no viole las leyes o regulaciones aplicables.",
            "O usuário é responsável por garantir que o uso do software não viole as leis ou regulamentos aplicáveis.",
            "Användaren ansvarar för att säkerställa att användningen av programvaran inte bryter mot tillämpliga lagar eller förordningar.",
            "Brukeren er ansvarlig for å sikre at bruken av programvaren ikke bryter med gjeldende lover eller forskrifter.",
            "Brukeren er ansvarlig for å sikre at bruken av programvaren ikke bryter med gjeldende lover eller forskrifter.",
            "Użytkownik jest odpowiedzialny za zapewnienie, że korzystanie z oprogramowania nie narusza obowiązujących przepisów prawa.",
            "Пользователь несет ответственность за то, чтобы использование программного обеспечения не нарушало применимые законы или нормативные акты.",
            "Користувач несе відповідальність за забезпечення того, що використання програмного забезпечення не порушує чинні закони або нормативні акти."
        ],
        23: [
            "Changes to terms of use:", "Änderungen der Nutzungsbedingungen:", "Modifiche ai termini di utilizzo:",
            "Changements aux conditions d'utilisation:", "Cambios en los términos de uso:",
            "Alterações nos termos de uso:", "Ändringar av användarvillkoren:", "Endringer i bruksvilkårene:",
            "Ændringer i brugsbetingelserne:", "Zmiany w warunkach użytkowania:", "Изменения в условиях использования:",
            "Зміни умов використання:"
        ],
        24: [
            "The developer reserves the right to change the terms of use at any time. It is the user's responsibility to regularly review the current terms.",
            "Der Entwickler behält sich das Recht vor, die Nutzungsbedingungen jederzeit zu ändern. Es liegt in der Verantwortung des Nutzers, sich regelmäßig über die aktuellen Bedingungen zu informieren.",
            "Lo sviluppatore si riserva il diritto di cambiare i termini di utilizzo in qualsiasi momento. È responsabilità dell'utente rivedere regolarmente i termini attuali.",
            "Le développeur se réserve le droit de modifier les conditions d'utilisation à tout moment. Il incombe à l'utilisateur de consulter régulièrement les conditions actuelles.",
            "El desarrollador se reserva el derecho de cambiar los términos de uso en cualquier momento. Es responsabilidad del usuario revisar regularmente los términos actuales.",
            "O desenvolvedor reserva-se o direito de alterar os termos de uso a qualquer momento. É responsabilidade do usuário revisar regularmente os termos atuais.",
            "Utvecklaren förbehåller sig rätten att ändra användarvillkoren när som helst. Det är användarens ansvar att regelbundet granska de aktuella villkoren.",
            "Utvikleren forbeholder seg retten til å endre bruksvilkårene når som helst. Det er brukerens ansvar å regelmessig gjennomgå de gjeldende vilkårene.",
            "Udvikleren forbeholder sig ret til at ændre brugsbetingelserne når som helst. Det er brugerens ansvar regelmæssigt at gennemgå de aktuelle betingelser.",
            "Deweloper zastrzega sobie prawo do zmiany warunków użytkowania w dowolnym momencie. Użytkownik jest odpowiedzialny za regularne przeglądanie aktualnych warunków.",
            "Разработчик оставляет за собой право изменять условия использования в любое время. Пользователь несет ответственность за регулярное ознакомление с текущими условиями.",
            "Розробник залишає за собою право змінювати умови використання в будь-який час. Користувач несе відповідальність за регулярний перегляд поточних умов."
        ],
        25: [
            "Please only use the software if you agree to the above conditions. If you do not agree to the terms, please refrain from using the software.",
            "Bitte nutzen Sie die Software nur, wenn Sie mit den oben genannten Bedingungen einverstanden sind. Falls Sie den Bedingungen nicht zustimmen, sehen Sie bitte von der Nutzung der Software ab.",
            "Si prega di utilizzare il software solo se si accettano le condizioni sopra indicate. Se non si accettano i termini, si prega di astenersi dall'utilizzare il software.",
            "Veuillez utiliser le logiciel uniquement si vous acceptez les conditions ci-dessus. Si vous n'acceptez pas les termes, veuillez ne pas utiliser le logiciel.",
            "Por favor, utilice el software solo si está de acuerdo con las condiciones mencionadas anteriormente. Si no está de acuerdo con los términos, por favor absténgase de usar el software.",
            "Por favor, use o software apenas se concordar com as condições acima. Se não concordar com os termos, por favor, não utilize o software.",
            "Använd programvaran endast om du godkänner ovanstående villkor. Om du inte godkänner villkoren, vänligen avstå från att använda programvaran.",
            "Bruk programvaren bare hvis du godtar de ovennevnte vilkårene. Hvis du ikke godtar vilkårene, vennligst avstå fra å bruke programvaren.",
            "Brug kun softwaren, hvis du accepterer de ovenstående betingelser. Hvis du ikke accepterer betingelserne, skal du undlade at bruge softwaren.",
            "Proszę korzystać z oprogramowania tylko, jeśli zgadzasz się z powyższymi warunkami. Jeśli nie zgadzasz się z warunkami, proszę powstrzymać się od korzystania z oprogramowania.",
            "Пожалуйста, используйте программное обеспечение только в том случае, если вы согласны с вышеуказанными условиями. Если вы не согласны с условиями, пожалуйста, воздержитесь от использования программного обеспечения.",
            "Будь ласка, використовуйте програмне забезпечення лише якщо ви згодні з вищезазначеними умовами. Якщо ви не згодні з умовами, утримуйтеся від використання програмного забезпечення."
        ],
        26: [
            "Please confirm that you have read and understood the disclaimer before proceeding.",
            "Bitte bestätigen Sie, dass Sie den Haftungsausschluss gelesen und verstanden haben, bevor Sie fortfahren.",
            "Si prega di confermare di aver letto e compreso l'esclusione di responsabilità prima di procedere.",
            "Veuillez confirmer que vous avez lu et compris la clause de non-responsabilité avant de continuer.",
            "Por favor, confirme que ha leído y comprendido el aviso legal antes de continuar.",
            "Por favor, confirme que leu e compreendeu a isenção de responsabilidade antes de continuar.",
            "Vänligen bekräfta att du har läst och förstått ansvarsfriskrivningen innan du fortsätter.",
            "Vennligst bekreft at du har lest og forstått ansvarsfraskrivelsen før du fortsetter.",
            "Bekræft venligst, at du har læst og forstået ansvarsfraskrivelsen, før du fortsætter.",
            "Proszę potwierdzić, że przeczytałeś i zrozumiałeś zrzeczenie się odpowiedzialności przed kontynuowaniem.",
            "Пожалуйста, подтвердите, что вы прочитали и поняли отказ от ответственности перед продолжением.",
            "Будь ласка, підтвердьте, що ви прочитали та зрозуміли застереження, перш ніж продовжити."
        ],
        27: [
            "I have read and accept the terms of the disclaimer.",
            "Ich habe den Haftungsausschluss gelesen und akzeptiere die Bedingungen.",
            "Ho letto e accetto i termini dell'esclusione di responsabilità.",
            "J'ai lu et j'accepte les termes de la clause de non-responsabilité.",
            "He leído y acepto los términos del aviso legal.",
            "Li e aceito os termos da isenção de responsabilidade.",
            "Jag har läst och accepterar villkoren i ansvarsfriskrivningen.",
            "Jeg har lest og aksepterer vilkårene i ansvarsfraskrivelsen.",
            "Jeg har læst og accepterer vilkårene for ansvarsfraskrivelse.",
            "Przeczytałem i akceptuję warunki zrzeczenia się odpowiedzialności.",
            "Я прочитал и принимаю условия отказа от ответственности.",
            "Я прочитав та приймаю умови застереження."
        ],
        28: [
            "Thank you! You can now use the software.",
            "Vielen Dank! Sie können die Software jetzt nutzen.",
            "Grazie! Ora puoi usare il software.",
            "Merci! Vous pouvez maintenant utiliser le logiciel.",
            "¡Gracias! Ahora puede usar el software.",
            "Obrigado! Agora você pode usar o software.",
            "Tack! Du kan nu använda programvaran.",
            "Takk! Du kan nå bruke programvaren.",
            "Tak! Du kan nu bruge softwaren.",
            "Dziękujemy! Możesz teraz używać oprogramowania.",
            "Спасибо! Теперь вы можете использовать программное обеспечение.",
            "Дякуємо! Тепер ви можете використовувати програмне забезпечення."
        ],
        29: [
            "You must accept the disclaimer to proceed.",
            "Sie müssen den Haftungsausschluss akzeptieren, um fortzufahren.",
            "Devi accettare l'esclusione di responsabilità per procedere.",
            "Vous devez accepter la clause de non-responsabilité pour continuer.",
            "Debe aceptar el aviso legal para continuar.",
            "Você deve aceitar a isenção de responsabilidade para continuar.",
            "Du måste acceptera ansvarsfriskrivningen för att fortsätta.",
            "Du må godta ansvarsfraskrivelsen for å fortsette.",
            "Du skal acceptere ansvarsfraskrivelsen for at fortsætte.",
            "Musisz zaakceptować zrzeczenie się odpowiedzialności, aby kontynuować.",
            "Вы должны принять отказ от ответственности, чтобы продолжить.",
            "Ви повинні прийняти застереження, щоб продовжити."
        ]

    }

    ########################################################################
    # Hintergrundfarbe von der APP
    Background_Style.run_background_styl()

    ########################################################################
    # st.image(r'https://cdn.pixabay.com/photo/2016/04/22/14/31/info-1345871_1280.png',width=100)
    # get the Agreemen-Value from Terms of Use checkbox
    if 'agree' not in st.session_state:
        agree = False
    else:
        agree = st.session_state.agree

    st.write('')
    st.write('')
    infos_spalte, sprache_spalte = st.columns([9, 1])
    with infos_spalte:

        # Haftungsausschluss-Text in Markdown-Format
        disclaimer = f"""
        # {translations_terms_of_use.get(2)[language_index]}

        {translations_terms_of_use.get(3)[language_index]} 

        ## {translations_terms_of_use.get(4)[language_index]}

        1. **{translations_terms_of_use.get(5)[language_index]}** {translations_terms_of_use.get(6)[language_index]}
        2. **{translations_terms_of_use.get(7)[language_index]}** {translations_terms_of_use.get(8)[language_index]}
        3. **{translations_terms_of_use.get(9)[language_index]}** {translations_terms_of_use.get(10)[language_index]}
        4. **{translations_terms_of_use.get(11)[language_index]}** {translations_terms_of_use.get(12)[language_index]}
        5. **{translations_terms_of_use.get(13)[language_index]}** {translations_terms_of_use.get(14)[language_index]}
        6. **{translations_terms_of_use.get(15)[language_index]}** {translations_terms_of_use.get(16)[language_index]}
        7. **{translations_terms_of_use.get(17)[language_index]}** {translations_terms_of_use.get(18)[language_index]}
        8. **{translations_terms_of_use.get(19)[language_index]}** {translations_terms_of_use.get(20)[language_index]}
        9. **{translations_terms_of_use.get(21)[language_index]}** {translations_terms_of_use.get(22)[language_index]}
        10. **{translations_terms_of_use.get(23)[language_index]}** {translations_terms_of_use.get(24)[language_index]}

        {translations_terms_of_use.get(25)[language_index]}
        """

        # Streamlit App
        st.title(f'{translations_terms_of_use.get(1)[language_index]}')
        st.markdown(disclaimer)

        if 'agree' not in st.session_state:
            st.session_state['agree'] = False
        else:
            st.session_state['agree'] = st.session_state.agree

        st.write(
            f'{translations_terms_of_use.get(26)[language_index]}')
        agree = st.checkbox(f'{translations_terms_of_use.get(27)[language_index]}',
                            value=st.session_state.agree)

        if agree:
            st.success(f'{translations_terms_of_use.get(28)[language_index]}')
            st.session_state['agree'] = True



        else:
            st.warning(f'{translations_terms_of_use.get(29)[language_index]}')
            st.session_state['agree'] = False

    with sprache_spalte:
        pass


