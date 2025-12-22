# PCIS Fantasy Stock Market Game

## Project Overview

The PCIS Fantasy Stock Market Game is an educational web application developed as part of the Prosper Center for Independent Study (PCIS) mentorship program. This platform provides students with a simulated stock market environment where they can learn investment principles, market dynamics, and portfolio management strategies without financial risk. The application enables users to practice buying and selling stocks using virtual currency, tracking their portfolio performance, and developing trading strategies in a controlled educational setting.

## Repository Information

**Repository:** https://github.com/TanishC4444/PCIS_FantasySMG  
**Project Type:** Educational Simulation Platform  
**Primary Framework:** Flask (Python Web Framework)  
**Development Status:** Active

## Educational Objectives

The platform is designed to support financial literacy education by providing hands-on experience with market concepts including portfolio diversification, risk assessment, market volatility, transaction costs, and long-term investment planning. Students can experiment with different trading strategies, analyze market trends, and understand the relationship between risk and return in a consequence-free environment that mirrors real-world market conditions.

## Technical Architecture

### Backend Framework

The application is built on Flask, a lightweight Python web framework that provides the routing, request handling, and response generation capabilities necessary for dynamic web applications. Flask was selected for its simplicity, flexibility, and extensive ecosystem of extensions that facilitate rapid development while maintaining code clarity and maintainability.

#### Flask Application Structure

The core application logic resides in app.py, which serves as the central entry point for the Flask application. This file defines the Flask application instance, configures application settings, establishes route handlers for various endpoints, and manages the request-response cycle. The Flask application follows the Model-View-Controller (MVC) architectural pattern, separating business logic from presentation concerns.

Route handlers in the Flask application process incoming HTTP requests, execute appropriate business logic, interact with data storage systems, and return rendered HTML templates or JSON responses. The application implements both GET and POST request methods, supporting standard web form submissions for user interactions such as account registration, stock purchase orders, and portfolio queries.

The Flask templating system utilizes Jinja2, a powerful template engine that enables dynamic HTML generation. Templates are stored in the templates directory and support template inheritance, allowing for consistent page layouts and reusable UI components. The base template structure typically includes navigation elements, common stylesheets, and JavaScript dependencies, while child templates extend this foundation with page-specific content.

#### Data Persistence and Storage

The application employs a file-based data storage strategy utilizing CSV (Comma-Separated Values) files for persistent data management. This approach provides simplicity and transparency during development while avoiding the overhead of database server administration. The primary data files include users.csv for user account information, sold.csv for transaction history, and balance.txt for tracking available virtual currency.

The users.csv file maintains user account records with fields for username, password (stored in hashed format for security), email address, account creation timestamp, and current cash balance. Each user record represents a registered participant in the simulation platform. The file-based approach enables straightforward data inspection and debugging during development phases.

Transaction records are preserved in sold.csv, documenting every stock purchase and sale executed within the platform. Each transaction entry captures essential information including username, stock symbol, transaction type (buy or sell), quantity of shares, price per share at transaction time, transaction timestamp, and resulting profit or loss for sale transactions. This comprehensive transaction log enables portfolio reconstruction, performance analysis, and historical reporting.

The balance.txt file serves as a simple persistent storage mechanism for tracking the virtual currency allocation within the system. This file-based approach allows for quick read and write operations without requiring complex database queries, though it presents limitations for concurrent access scenarios that would be addressed in production deployments through database transaction management.

### Data Processing and Business Logic

#### User Authentication System

User authentication is implemented through session-based authentication mechanisms provided by Flask's session management capabilities. When users submit login credentials through the authentication form, the application retrieves the corresponding user record from users.csv, verifies the provided password against the stored hash using secure hashing algorithms, and establishes an authenticated session upon successful validation.

Password security is maintained through cryptographic hashing, transforming plaintext passwords into irreversible hash values before storage. The hashing process incorporates salt values to defend against rainbow table attacks and ensures that identical passwords produce different hash values across different user accounts. The hashing algorithm selection prioritizes security over performance, typically employing bcrypt or similar adaptive hashing functions that resist brute-force attacks through computational intensity.

Session management utilizes server-side session storage, maintaining user authentication state across multiple HTTP requests. Upon successful authentication, the application generates a session identifier, stores session data on the server, and returns a session cookie to the client browser. Subsequent requests include this session cookie, enabling the application to retrieve session data and verify authentication status without requiring repeated credential submission.

Session security measures include secure cookie flags, HTTP-only cookie attributes to prevent JavaScript access, and session timeout mechanisms to automatically invalidate sessions after periods of inactivity. The application implements authorization checks at route handler entry points, verifying authenticated status before processing sensitive operations such as trade execution or portfolio viewing.

#### Stock Market Data Integration

The platform simulates stock market conditions by integrating real-time or near-real-time market data through external financial data APIs. While the specific API provider may vary based on availability and licensing considerations, common sources include Alpha Vantage, Yahoo Finance, or IEX Cloud, which provide programmatic access to stock quotes, historical prices, and company information.

API integration is implemented through Python's requests library, which facilitates HTTP communication with external services. The application constructs API requests with appropriate parameters including stock symbols, data granularity, and authentication credentials. Response data, typically delivered in JSON format, undergoes parsing and validation before integration into application logic.

Data caching strategies optimize API usage and application performance by storing frequently accessed market data in memory or temporary storage. Cache invalidation policies ensure data freshness by expiring cached values after predetermined intervals, balancing the competing demands of up-to-date information and API rate limit compliance. The caching layer reduces redundant API calls for commonly viewed stocks, improving response times and reducing external service dependencies.

Error handling mechanisms account for API unavailability, rate limiting, and data inconsistencies. The application implements retry logic with exponential backoff for transient failures, fallback to cached data when fresh data is unavailable, and graceful degradation to maintain core functionality even when external services experience disruptions.

#### Portfolio Management and Trade Execution

Portfolio management functionality enables users to maintain collections of stock positions, tracking ownership quantities, purchase prices, current market values, and unrealized gains or losses. The portfolio calculation engine aggregates individual positions, computing total portfolio value by combining current stock holdings with available cash balances.

Trade execution logic processes buy and sell orders submitted by users through the trading interface. Purchase orders validate available cash balances, verify order quantities exceed minimum thresholds, confirm stock symbol validity through market data lookup, and calculate total transaction costs including commission fees if applicable. Upon validation, the system deducts purchase costs from cash balances, records new stock positions or increments existing positions, and logs transaction details to the transaction history file.

Sale orders verify ownership of sufficient share quantities, retrieve current market prices for valuation, calculate sale proceeds and realized gains or losses, update portfolio positions by reducing or eliminating holdings, credit sale proceeds to cash balances, and record transaction details including profit or loss calculations. The profit calculation determines realized gains by comparing sale proceeds against original purchase costs for the specific shares being sold.

Commission and fee structures can be incorporated into transaction processing to simulate real-world trading costs. Fixed-rate commissions, percentage-based fees, or tiered pricing models deduct specified amounts from transaction proceeds or add costs to purchase totals, teaching users about the impact of transaction costs on investment returns.

#### Performance Analytics and Reporting

Performance measurement capabilities enable users to evaluate trading success through various metrics including total portfolio value over time, percentage returns relative to starting capital, comparison against market indices or benchmark performance, transaction count and trading frequency, win-loss ratios comparing profitable to unprofitable trades, and average holding periods for positions.

The reporting system generates portfolio summaries displaying current holdings with quantities, purchase prices, current market values, and unrealized gains or losses for each position. Transaction history reports present chronological listings of all trades executed, enabling users to review trading decisions and identify patterns in their investment behavior.

Graphical visualizations enhance data comprehension through charts depicting portfolio value trends over time, allocation pie charts showing diversification across different stocks or sectors, and performance comparison graphs contrasting user returns against relevant benchmarks. These visual elements support data-driven learning and strategic refinement.

### Frontend Implementation

The frontend interface is constructed using standard web technologies including HTML5 for semantic document structure, CSS3 for styling and visual presentation, and JavaScript for client-side interactivity and dynamic content updates. The index.html file serves as the primary entry point, implementing the main application interface through which users navigate to various features.

Template rendering through Flask's Jinja2 integration enables server-side generation of dynamic HTML content. Templates receive data from Flask route handlers through template context variables, which are then interpolated into HTML markup using Jinja2's template syntax. This approach supports personalized content presentation, conditional rendering based on user state, and iteration over collections such as portfolio holdings or transaction records.

Form handling facilitates user input collection for operations including user registration, authentication, stock symbol lookup, and trade order submission. Forms implement client-side validation through HTML5 input attributes and JavaScript validation functions, providing immediate feedback on input errors before server submission. Server-side validation in Flask route handlers provides defense-in-depth security by verifying input constraints regardless of client-side validation bypass attempts.

JavaScript enhancement provides interactive features such as real-time stock price updates through asynchronous API requests, dynamic form field validation with inline error messaging, autocomplete functionality for stock symbol entry, and interactive charts for performance visualization. The application may utilize JavaScript frameworks or libraries to streamline development, though the specific implementation details depend on project complexity and developer preferences.

### Dependencies and Environment Management

The req.txt file enumerates Python package dependencies required for application execution. This requirements file enables reproducible environment setup through Python's pip package manager, which installs specified packages and their transitive dependencies in development and deployment environments.

Key dependencies include Flask for web application framework functionality, pandas for data manipulation and CSV file processing, requests for HTTP client operations and API integration, and potentially additional packages for authentication, data visualization, or enhanced functionality. Version specifications in the requirements file ensure consistent behavior across different deployment environments by pinning exact package versions or constraining version ranges.

Virtual environment usage is standard practice for Python development, isolating project dependencies from system-wide Python installations and preventing version conflicts between different projects. The project documentation should include instructions for creating and activating virtual environments using venv or virtualenv tools, installing dependencies from req.txt, and running the Flask development server.

### Testing Infrastructure

The test.py file suggests the presence of automated testing infrastructure for validating application functionality. Testing strategies for web applications typically encompass unit tests for individual functions and methods, integration tests for component interactions and data flow, and functional tests simulating user interactions through the web interface.

Unit tests verify isolated components such as authentication functions, portfolio calculation logic, and data parsing routines. These tests execute rapidly and provide fast feedback during development, enabling test-driven development practices and regression detection. Mock objects and fixtures simulate external dependencies such as API responses or file system operations, allowing tests to run independently of external services.

Integration tests validate interactions between application layers including request routing to correct handlers, template rendering with appropriate context data, and database operations persisting and retrieving records correctly. These tests exercise larger portions of the application stack, ensuring components integrate properly while remaining independent of full application deployment.

## Firebase Integration Architecture

While the current implementation utilizes file-based storage, the application architecture is designed to support migration to Firebase for enhanced scalability, real-time capabilities, and production-grade reliability. Firebase provides comprehensive backend-as-a-service functionality including authentication, database, hosting, and analytics capabilities that can significantly enhance the platform's capabilities.

### Firebase Realtime Database Implementation

Firebase Realtime Database would serve as the primary data store, replacing CSV-based file storage with a cloud-hosted NoSQL database that supports real-time synchronization and offline capabilities. The database structure would organize data hierarchically in JSON format, creating collections for users, portfolios, transactions, and market data caches.

The users collection would store user profiles with unique identifiers serving as keys, eliminating the current linear search requirements of CSV files. Each user node would contain authentication-related fields (delegated to Firebase Authentication), profile information, account settings, and references to associated portfolio and transaction data. The hierarchical structure enables efficient retrieval of user-specific data through direct path queries.

Portfolio data would be organized under user-specific nodes, storing current holdings as child objects indexed by stock symbol. Each holding object would track quantity owned, average purchase price, total cost basis, and acquisition timestamps. This structure enables atomic updates to individual holdings without requiring full file rewrites, significantly improving concurrent access performance.

Transaction history would maintain chronological records under user-specific nodes, with individual transaction objects containing all relevant details. The timestamp-based keys enable efficient range queries for retrieving transactions within specific date ranges, supporting filtered transaction history views and temporal analysis.

Real-time listeners would be established on portfolio and market data nodes, enabling automatic UI updates when data changes occur. When users execute trades or when market prices update, all connected clients receive immediate notifications through WebSocket connections maintained by the Firebase SDK, eliminating the need for polling or manual refresh operations.

Security rules would be configured to enforce data access policies at the database level. Rules would restrict read and write access to authenticated users, ensure users can only access their own portfolio data, allow public read access to market data caches while restricting writes to administrative processes, and validate data structure and content before accepting writes. These server-enforced rules provide defense-in-depth security independent of client-side validation.

### Firebase Authentication Integration

Firebase Authentication would replace the custom session-based authentication system with industry-standard identity management. The platform supports multiple authentication methods including email and password authentication as the primary mechanism, Google OAuth for single sign-on integration, anonymous authentication for guest browsing, and custom token authentication for integration with existing identity systems.

Email and password authentication provides familiar registration and login flows while delegating password storage, hashing, and verification to Firebase's secure infrastructure. User registration through the Firebase Authentication API creates secure accounts without exposing password handling logic in application code. The authentication system automatically implements security best practices including adaptive hashing algorithms, rate limiting to prevent brute force attacks, and secure token generation and validation.

The authentication flow begins when users submit credentials through the login form. The client-side Firebase SDK communicates directly with Firebase Authentication services to verify credentials and obtain authentication tokens. Upon successful authentication, Firebase returns a JSON Web Token (JWT) that serves as proof of identity for subsequent requests. This token is automatically included in all Firebase service requests through SDK integration.

Token management handles automatic refresh before expiration, ensuring uninterrupted user sessions without requiring repeated authentication. The refresh token mechanism operates transparently, requesting new authentication tokens from Firebase before current tokens expire. This approach balances security requirements for limited token validity with user experience expectations for persistent sessions.

Session persistence utilizes browser local storage or session storage to maintain authentication state across page reloads and browser sessions. The Firebase SDK manages token storage securely, employing storage mechanisms appropriate for the token sensitivity and session duration requirements. Developers can configure session persistence behavior to support different use cases from temporary sessions that expire upon browser closure to long-lived sessions that persist across browser restarts.

Security rules integration with Firebase Authentication enables database access control based on authenticated user identity. Database security rules reference the authenticated user's unique identifier (UID) provided in the authentication context, enabling user-specific data isolation and permission enforcement. Rules can verify that users only access their own portfolio data, preventing unauthorized information disclosure or data manipulation.

Multi-factor authentication (MFA) support can be enabled to enhance account security for users opting into additional protection. MFA requires users to provide secondary verification through SMS codes, authenticator app tokens, or hardware security keys before completing authentication, significantly increasing account security against credential compromise.

### Firebase Cloud Functions for Backend Logic

Firebase Cloud Functions would provide serverless compute capabilities for implementing backend business logic that should not execute on the client. These functions respond to HTTP requests, database triggers, authentication events, and scheduled operations, enabling implementation of secure transaction processing, automated market data updates, portfolio rebalancing operations, and administrative functions.

Transaction processing functions would handle buy and sell order execution through HTTPS callable functions invoked from client applications. These functions receive order parameters including stock symbol, transaction type, and quantity, validate user authentication and authorization, verify sufficient cash balances for purchases or share ownership for sales, query current market prices from external APIs, calculate transaction costs and updated portfolio positions, atomically update user balances and portfolio holdings in the database, record transaction history, and return transaction confirmation or error details.

The serverless execution model ensures functions scale automatically based on demand, handling concurrent requests from multiple users without capacity planning or server management. Functions execute in isolated environments with their own authentication contexts, preventing cross-contamination between user requests.

Database trigger functions respond automatically to data changes, implementing reactive business logic without requiring explicit invocation. A trigger function might execute when a new user registers, initializing their portfolio with starting cash balances and default holdings. When transactions are recorded, triggers could update aggregated statistics, send notification emails, or update leaderboard rankings.

Scheduled functions execute on predefined intervals for maintenance operations. A scheduled function running hourly or daily could fetch updated market data from external APIs, refresh cached price information in the database, calculate portfolio values for all users based on current prices, generate performance reports and analytics, and archive old transaction data. These automated processes ensure data freshness and system health without manual intervention.

Security is maintained through Firebase Security Rules on the database level and function-level authentication verification. Cloud Functions can verify ID tokens included in request headers, ensuring only authenticated and authorized users can invoke specific functions. This server-side verification is immune to client-side tampering, providing reliable access control.

### Firebase Hosting and Deployment

Firebase Hosting would provide static file hosting for the frontend application assets including HTML, CSS, JavaScript, images, and other resources. The hosting service delivers content through a global content delivery network (CDN), ensuring low-latency access for users regardless of geographic location.

Deployment workflows integrate with version control systems through Firebase CLI tools. Developers execute deployment commands that upload updated assets to Firebase Hosting, with automatic cache invalidation ensuring users receive the latest version. The platform supports deployment rollback capabilities, enabling quick recovery from problematic deployments by reverting to previous versions.

Custom domain configuration enables the application to operate under a branded domain rather than the default Firebase subdomain. SSL certificate provisioning is automated through Firebase's integration with certificate authorities, providing HTTPS encryption for all hosted content without manual certificate management.

### Real-Time Data Synchronization

The Firebase Realtime Database's core capability is real-time data synchronization across all connected clients. When portfolio values update due to market price changes or when users execute trades that affect leaderboard rankings, all clients viewing affected data receive immediate updates through open WebSocket connections.

This real-time synchronization transforms the user experience from traditional request-response patterns to collaborative, live-updating interfaces. Users observing market dashboards see price updates flow in continuously without refresh actions. Leaderboards update dynamically as participants execute trades, creating engaging competitive dynamics.

Offline capabilities ensure application functionality continues when network connectivity is lost. The Firebase SDK maintains a local cache of recently accessed data, enabling read operations to complete successfully against cached data. Write operations queue locally and automatically synchronize when connectivity restores, ensuring no data loss during temporary disconnections.

Conflict resolution mechanisms handle scenarios where multiple clients modify the same data while offline or in rapid succession. Firebase employs last-write-wins semantics by default, though developers can implement custom conflict resolution logic for scenarios requiring more sophisticated merge strategies.

### Firebase Analytics and Monitoring

Firebase Analytics provides comprehensive usage tracking and user behavior analysis without requiring custom analytics implementation. The platform automatically captures user engagement metrics including daily active users, session duration, screen views, and user retention rates. Custom event tracking enables monitoring of domain-specific actions such as trade execution frequency, portfolio performance milestones, and feature usage patterns.

Performance monitoring tracks application load times, network latency, and function execution duration, identifying performance bottlenecks and degradation over time. Crash reporting captures client-side errors with stack traces, enabling rapid issue diagnosis and resolution. These monitoring capabilities inform optimization priorities and validate the impact of performance improvements.

## Deployment Considerations

### Development Environment Setup

Developers setting up local development environments should install Python 3.7 or higher, create and activate a Python virtual environment, install dependencies from req.txt using pip, configure environment variables for API keys and secrets, initialize data files with appropriate schema, and execute the Flask development server through standard flask run commands or python app.py invocations.

### Production Deployment

Production deployment requires considerations for security, performance, scalability, and reliability that extend beyond development environment configurations. Flask's built-in development server is unsuitable for production traffic due to performance limitations and security deficiencies. Production deployments should employ WSGI-compliant application servers such as Gunicorn or uWSGI, which provide concurrent request handling through worker processes or threads.

Web server configuration typically places a reverse proxy such as Nginx or Apache in front of the application server, handling SSL termination, static file serving, request load balancing, and DDoS protection. The reverse proxy forwards dynamic requests to the application server while serving static assets directly from the file system, improving overall system efficiency.

Environment variable management externalizes configuration from application code, enabling different settings across development, staging, and production environments without code modifications. Sensitive credentials such as API keys, database passwords, and encryption keys should never be committed to version control, instead being injected through environment variables or secure secret management services.

Database migration from file-based storage to production database systems such as PostgreSQL, MySQL, or cloud database services is essential for reliability, concurrent access support, transaction integrity, and backup capabilities. The migration process involves schema design to represent current data structures, data migration scripts to transfer existing records, and application code updates to use database client libraries instead of direct file operations.

Monitoring and logging infrastructure provides visibility into application health, performance metrics, error rates, and security events. Application performance monitoring (APM) tools track request latency, throughput, and error rates, while centralized logging aggregates log messages from distributed application instances for analysis and troubleshooting.

### Scalability Considerations

As user populations grow, the application must scale to maintain acceptable performance and reliability. Horizontal scaling through multiple application server instances distributed across load balancers provides increased capacity and fault tolerance. Session state management must account for distributed architectures through centralized session storage in Redis or database systems, enabling any application instance to handle requests from any user.

Database scaling strategies include read replicas for distributing query load, connection pooling to efficiently manage database connections, query optimization through indexing and query rewriting, and caching frequently accessed data in memory stores. For extreme scale requirements, database sharding partitions data across multiple database instances, though this introduces significant complexity in query routing and transaction management.

## Security Considerations

Security is paramount for applications handling user accounts, financial simulations, and personal information. Authentication and authorization mechanisms must prevent unauthorized access, session hijacking, and privilege escalation. Input validation protects against injection attacks by sanitizing user inputs and using parameterized queries for database operations. Cross-site scripting (XSS) prevention employs output encoding when rendering user-supplied content in HTML context. Cross-site request forgery (CSRF) protection uses token-based validation to ensure requests originate from legitimate application pages.

Data encryption protects sensitive information in transit through HTTPS/TLS and at rest through database encryption and encrypted file systems. Regular security audits, dependency vulnerability scanning, and penetration testing identify and remediate security weaknesses before exploitation.

## Educational Features and Learning Outcomes

The platform supports educational objectives through various mechanisms. Tutorial content guides new users through account creation, navigation, stock research, and trade execution. Tooltips and explanatory text throughout the interface provide contextual learning opportunities. Achievement systems reward successful trading strategies and learning milestones, encouraging engagement and skill development.

Performance analytics enable self-assessment and strategy refinement. Students can review their trading history, analyze wins and losses, and identify patterns in their decision-making. Comparison against peers or market indices provides benchmarking context for evaluating personal performance.

Simulated market scenarios can introduce students to various market conditions including bull markets, bear markets, high volatility periods, and sector-specific events. These scenarios teach adaptability and risk management in changing market environments.

## Future Enhancement Opportunities

The platform architecture supports numerous potential enhancements including real-time market data integration for immediate price updates, mobile application development for iOS and Android platforms, social features enabling collaboration and competition among users, educational content integration providing lessons on investment strategies and financial concepts, options and derivatives trading to introduce advanced financial instruments, portfolio analysis tools offering deeper insights into risk and diversification, and machine learning integration for predictive analytics and trading recommendations.

## License and Usage

This project is developed for educational purposes as part of the PCIS mentorship program. Usage and distribution are subject to institutional policies and applicable software licenses.

---

**Developed by:** TanishC4444  
**Project Status:** Active Development  
