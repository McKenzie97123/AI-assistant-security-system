WYŻSZA SZKOŁA ZARZĄDZANIA I BANKOWOŚCI W KRAKOWIE 

Wydział Nauk Stosowanych 

KIERUNEK: Informatyka Stosowana 

ZAKRES KSZTAŁCENIA: Software engineering i produkcja oprogramowania 

PRACA DYPLOMOWA 

Michał Jerzy Kubera 

Współczesne metody zabezpieczenia witryn internetowych przed botami spamerskimi 
 

PROMOTOR: 

dr inż. Darin Nikolow 

KRAKÓW 2026
SPIS TRESCI 

​​ 

​ 

​ 

​ 

​ 

​ 

​ 

​ 

​ 

​ 

​ 

​ 

​ 

​​ 

 

Streszczenie pracy 

Celem niniejszej pracy jest analiza nowoczesnych rozwiązań służących ochronie aplikacji internetowych przed zautomatyzowanymi atakami botów spamerskich. Impulsem do podjęcia tematu jest rosnąca dostępność zaawansowanych modeli sztucznej inteligencji, które mogą być wykorzystywane do analizy zachowań użytkowników w środowisku webowym, a tym samym stanowić skuteczny mechanizm zwiększający poziom bezpieczeństwa oraz stabilności aplikacji internetowych. 

Głównym aspektem pracy jest zbadanie możliwości wykorzystania sztucznej inteligencji do analizy danych sieciowych oraz logiki zapytań HTTP w celu identyfikacji i blokowania zautomatyzowanych ataków. Szczególną uwagę poświęcono analizie wpływu skalowania infrastruktury ataku na efektywność zastosowanych mechanizmów zabezpieczających oraz ocenie skuteczności modelu sztucznej inteligencji w warunkach zwiększonego obciążenia. 

W części eksperymentalnej przygotowano zamknięte, skalowalne środowisko testowe oparte na technologii konteneryzacji. W środowisku tym uruchomiono rozproszone instancje botów spamerskich symulujących zautomatyzowany atak na aplikację internetową. Aplikacja webowa została wdrożona w odseparowanym kontenerze oraz zintegrowana z modelem sztucznej inteligencji odpowiedzialnym za analizę ruchu i wykrywanie podejrzanych wzorców zachowań. 

Liczba botów oraz ich podstawowa konfiguracja stanowiły wartość stałą, natomiast zmienną badawczą były mechanizmy zabezpieczające oraz konfiguracja modelu sztucznej inteligencji. Celem badań było określenie skuteczności opracowanego rozwiązania w zależności od przyjętych parametrów ochrony oraz warunków obciążeniowych. 

 

Abstract 

The aim of this thesis is to analyze modern solutions for protecting web applications against automated spam bot attacks. The motivation for undertaking this research stems from the increasing availability of advanced artificial intelligence models, which can be used to analyze user behavior in web environments and thereby serve as effective mechanisms for enhancing the security and stability of web applications. 

The main focus of this work is to examine the potential of artificial intelligence in analyzing network traffic data and HTTP request logic in order to detect and mitigate automated attacks. Particular attention is given to evaluating the impact of scaling the attack infrastructure on the effectiveness of implemented security mechanisms, as well as assessing the performance of the artificial intelligence model under increased load conditions. 

In the experimental part of the study, a closed and scalable test environment based on containerization technology was prepared. Within this environment, distributed instances of spam bots were deployed to simulate automated attacks targeting a web application. The web application was deployed in an isolated container and integrated with an artificial intelligence model responsible for traffic analysis and suspicious behavior detection. 

The number of bots and their baseline configuration remained constant, while the security mechanisms and the configuration of the artificial intelligence model constituted the independent research variables. The objective of the experiments was to determine the effectiveness of the proposed solution depending on the selected protection parameters and system load conditions. 

 

1. Wstęp 

Dynamiczny rozwój technologii informatycznych oraz rosnąca dostępność narzędzi sztucznej inteligencji istotnie wpływają na sposób funkcjonowania współczesnych aplikacji internetowych. Internetowe systemy informatyczne stanowią obecnie podstawę działalności wielu przedsiębiorstw, instytucji publicznych oraz platform usługowych. Wraz ze wzrostem ich znaczenia zwiększa się również potrzeba zapewnienia wysokiego poziomu bezpieczeństwa, niezawodności oraz odporności na zagrożenia wynikające z automatyzacji ruchu sieciowego. Jednym z istotnych problemów pozostają zautomatyzowane działania realizowane przez boty spamerskie, które mogą zakłócać funkcjonowanie aplikacji internetowych. 

Szczególnym wyzwaniem dla bezpieczeństwa aplikacji webowych jest rosnąca skala i złożoność ruchu generowanego w środowiskach sieciowych. Współczesne aplikacje są zmuszone obsługiwać dużą liczbę równoczesnych zapytań, przy jednoczesnym zachowaniu wysokiej dostępności usług dla użytkowników. W takich warunkach tradycyjne metody ochronne mogą się okazać niewystarczające lub negatywnie wpływać na stabilność aplikacji webowej a co się z tym wiąże na komfort korzystania z aplikacji. 

W odpowiedzi na te wyzwania coraz większe znaczenie zyskują rozwiązania oparte na zastosowaniu sztucznej inteligencji, umożliwiające analizę, danych sieciowych czy logikę zapytań HTTP. Modele sztucznej inteligencji tym samym mogą posłużyć nam w analizie, której zadaniem będzie identyfikacja nietypowych wzorców aktywności w sposób adaptacyjny i dynamiczny. 

W kontekście rosnącej liczby zagrożeń oraz dynamicznie zmieniających się warunków pracy aplikacji internetowych zasadne jest przeprowadzenie analizy skuteczności mechanizmów ochronnych wspieranych przez sztuczną inteligencję. Niniejsza praca podejmuje próbę zbadania tego zagadnienia w kontrolowanym, skalowalnym środowisku eksperymentalnym, umożliwiającym ocenę działania modelu w warunkach zwiększonego obciążenia. 

1.1 Cel pracy 

Celem niniejszej pracy była analiza skuteczności nowoczesnych metod ochrony aplikacji internetowych przed zautomatyzowanymi atakami botów spamerskich z wykorzystaniem modelu sztucznej inteligencji. 

W ramach pracy stworzone zostało zamknięte środowisko badawcze umożliwiające symulację ataku cybernetycznego na aplikację internetową. W środowisku tym zastosowano model sztucznej inteligencji pełniący funkcję analizatora danych generowanych w obrębie witryny, który na podstawie analizy ruchu sieciowego oraz wzorców zapytań podejmował działania zapobiegające atakom. Zaimplementowano również boty spamerskie stanowiące stały, kontrolowany model ataku na aplikację webową, a także samą aplikację internetową poddaną testom.  

W celu stworzenia izolowanego i w pełni kontrolowanego środowiska testowego wykorzystano technologię Kubernetes, umożliwiając zarządzanie konteneryzowanymi komponentami systemu. Zastosowanie tej technologii pozwoliło nie tylko na zapewnienie separacji poszczególnych elementów infrastruktury, lecz również na uzyskanie skalowalności środowiska — zarówno w zakresie liczby instancji botów, komponentów modelu sztucznej inteligencji, jak i samej aplikacji webowej. 

Utworzone środowisko posłużyło do przeprowadzenia badań nad skutecznością modelu sztucznej inteligencji jako mechanizmu ochrony aplikacji internetowej przed botami spamerskimi. Zmienną badawczą była konfiguracja modelu sztucznej inteligencji oraz zastosowane metody ochrony witryny, natomiast elementem stałym pozostawał zestaw botów spamerskich generujących ruch testowy. Skuteczność opracowanego rozwiązania oceniano na podstawie określonych metryk, takich jak wykrywalność zautomatyzowanego ruchu, odporność systemu na zwiększone obciążenie oraz wpływ zastosowanych zabezpieczeń na dostępność i stabilność aplikacji. 

1.2 Zawartość pracy 

W pracy przedstawiono teoretyczne podstawy związane z wykorzystaniem sztucznej inteligencji w kontekście cyberbezpieczeństwa, wraz ze szczególnym uwzględnieniem automatyzacji ataków na aplikacje internetowe. Omówiono również współczesne zagrożenia wynikające z wykorzystania botów oraz techniki ich wykrywania i neutralizacji.  

Kolejna część pracy obejmuje opis środowiska badawczego, wykorzystane technologie oraz sposób konfiguracji systemu opartego kontenerach. Szczegółowe przedstawienie mechanizmów działania agentów sztucznej inteligencji oraz zastosowanie metod ochronnych w testowanej aplikacji. 

W części eksperymentalnej zaprezentowano przebieg przeprowadzonych testów, zastosowaną metodologię badawczą oraz analizę uzyskanych wyników. Ostatni rozdział zawiera podsumowanie rezultatów, ocenę skuteczności badanych mechanizmów ochronnych oraz propozycje dalszych kierunków badań w obszarze zabezpieczania aplikacji internetowych przed atakami wspieranymi przez sztuczną inteligencje.  

2. Istniejące metody ochrony aplikacji webowych 

W tym rozdziale przedstawiono istniejące rozwiązania technologiczne stosowane w ochronie aplikacji webowych przed atakami cybernetycznymi. Wraz z rozwojem technologii oraz rosnącą zaawansowaniem botów spamerskich, tradycyjne metody zabezpieczania witryn internetowych musiały ulec dostosowaniu, aby skutecznie przeciwdziałać nowym formom zautomatyzowanych zagrożeń. 

2.1 Metody ochrony aplikacji webowych przed botami spamerskimi 

Rynek aplikacji samochodowych nie jest ukierunkowany na aspekty wyszczególnione w mojej pracy, takie jak prowadzenie dokumentacji oraz zapis zdarzeń dla danego pojazdu. Popularne aplikacje wprowadzane na rynek głównie skupiają się na poprawie komfortu kierowcy poprzez dostarczaniu informacji o zdarzeniach znajdujących się na drodze.  

2.1.1 reCAPTCHA 

reCAPTCHA jest jednym z najczęściej stosowanych mechanizmów weryfikacji użytkownika, mającym na celu odróżnienie człowieka od bota. System ten opiera się na analizie zachowań użytkownika, takich jak sposób poruszania myszką czy czas interakcji z formularzem, a także na klasycznych zadaniach typu „kliknij wszystkie obrazki zawierające…”. Dzięki dynamicznemu dostosowywaniu poziomu trudności, reCAPTCHA utrudnia automatyczne wypełnianie formularzy przez boty. Jednocześnie rozwiązanie to jest stosunkowo łatwe do wdrożenia w aplikacjach webowych, co czyni je popularnym wyborem wśród deweloperów. 

2.1.2 Ograniczenie liczby zapytań (Rate Limiting) 

Ograniczenie liczby zapytań do serwera w określonym czasie jest jedną z podstawowych metod ochrony przed zautomatyzowanym ruchem. Poprzez kontrolowanie częstotliwości wysyłania żądań, mechanizm ten pozwala na ograniczenie możliwości masowego przesyłania formularzy czy prób logowania, minimalizując skutki działań botów. Dodatkowo, system może wykrywać nadmierną aktywność z określonych adresów IP i tymczasowo blokować podejrzane źródła. Metoda ta jest efektywna w prostych scenariuszach ataków, jednak może być mniej skuteczna wobec botów wykorzystujących zmienne adresy IP lub rozproszone infrastruktury. 

2.1.3 Wykrywanie anomalii ruchu sieciowego 

Systemy wykrywania anomalii analizują ruch sieciowy pod kątem nietypowych wzorców, takich jak powtarzalne zapytania z tego samego adresu IP czy nagłe skoki liczby żądań. Mechanizmy te mogą automatycznie blokować podejrzany ruch lub kierować go do dodatkowej weryfikacji, co zwiększa odporność aplikacji na zautomatyzowane ataki. Analiza anomalii pozwala również na identyfikację nowych, wcześniej nieznanych sposobów działania botów. W połączeniu z innymi mechanizmami ochronnymi, metoda ta znacząco podnosi bezpieczeństwo aplikacji webowych. 

2.1.4 Weryfikacja sesji i tokeny CSRF 

Stosowanie tokenów CSRF (Cross-Site Request Forgery) oraz mechanizmów weryfikacji sesji pozwala na ograniczenie ryzyka wykorzystania aplikacji przez nieautoryzowane boty. Tokeny generowane dla każdej sesji uniemożliwiają automatyczne wysyłanie żądań z zewnątrz i wymagają interakcji użytkownika, co utrudnia przeprowadzanie zautomatyzowanych ataków. Mechanizmy te zwiększają integralność sesji użytkownika oraz zapobiegają manipulacjom w danych przesyłanych w formularzach. Są one szczególnie przydatne w aplikacjach webowych przetwarzających poufne dane lub umożliwiających wykonywanie operacji finansowych. 

2.2 Analiza współczesnych metod ochrony 

Przedstawione metody ochrony aplikacji webowych przed botami spamerskimi, takie jak reCAPTCHA, ograniczenie liczby zapytań, wykrywanie anomalii ruchu sieciowego czy weryfikacja sesji i tokeny CSRF, mają wspólny cel: zapewnienie bezpieczeństwa aplikacji poprzez odróżnienie ruchu legalnego od zautomatyzowanego. 

Czynnikami wspólnymi wszystkich metod jest prewencja, monitorowanie oraz ograniczanie skutków ataków. Mechanizmy te dążą do minimalizacji ryzyka związanego z masowym ruchem botów, ochrony integralności danych oraz utrzymania dostępności aplikacji dla prawdziwych użytkowników. Ponadto każda z metod wymaga ciągłego dostosowywania do nowych technik wykorzystywanych przez boty — co oznacza, że skuteczna ochrona aplikacji webowej jest procesem dynamicznym, a nie jednorazowym działaniem.
 

Analiza tych metod pokazuje również, że tradycyjne podejścia, oparte głównie na prostych filtrach czy ograniczeniach ilościowych, mogą być niewystarczające wobec coraz bardziej zaawansowanych botów. W związku z tym coraz większe znaczenie zyskują rozwiązania adaptacyjne i inteligentne, które wykorzystują analizę wzorców zachowań i uczenie maszynowe do przewidywania oraz blokowania niepożądanego ruchu w czasie rzeczywistym.  

2.3 Kierunki rozwoju metod ochrony 

Współczesne metody ochrony aplikacji webowych ewoluują w kierunku rozwiązań adaptacyjnych i inteligentnych, które potrafią wykrywać zautomatyzowany ruch w czasie rzeczywistym. Coraz większe znaczenie zyskują systemy oparte na sztucznej inteligencji i uczeniu maszynowym, które analizują wzorce zachowań użytkowników i potrafią odróżnić boty od prawdziwych użytkowników nawet w przypadku wyrafinowanych ataków. 

Równocześnie obserwuje się wzrost zainteresowania rozproszonymi mechanizmami detekcji, które monitorują ruch w wielu punktach aplikacji oraz integrują informacje z różnych źródeł, co pozwala szybciej reagować na nowe zagrożenia. Istotnym trendem jest także analiza behawioralna, która zamiast bazować wyłącznie na statycznych regułach, uczy się charakterystycznych wzorców interakcji użytkowników, co zwiększa skuteczność wykrywania botów. 

W przyszłości oczekuje się dalszego rozwoju systemów hybrydowych, łączących tradycyjne metody ochrony z inteligentnymi mechanizmami predykcyjnymi. Takie podejście pozwoli nie tylko na skuteczniejszą ochronę aplikacji, ale także na minimalizację wpływu zabezpieczeń na doświadczenie prawdziwych użytkowników. Trendy te wskazują, że skuteczna ochrona aplikacji webowych stanie się coraz bardziej zależna od połączenia prewencji, monitorowania i adaptacyjnych mechanizmów wykrywania.
 

3. Architektura środowiska testowego 

4. Wdrożenie i konfiguracja środowiska testowego 

5. Wyniki testu oraz analiza skuteczności 

6. Podsumowanie 

 

 

Bibliografia 

Książki 

XXX 

Netografia 

XXX 

Artykuły i dokumenty 

XXX 

Spis ilustracji i listingów 

XXX 