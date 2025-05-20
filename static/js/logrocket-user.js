// Función para inicializar LogRocket con identificación de usuario
function initializeLogRocketWithUser(userData) {
    if (!window.LogRocket) {
        console.error('LogRocket no está inicializado');
        return;
    }

    // Inicializar LogRocket
    window.LogRocket.init('1dtbnm/trabajo_final');

    // Si tenemos datos del usuario
    if (userData && userData.id) {
        // Identificar al usuario con sus datos completos
        window.LogRocket.identify(userData.id, {
            name: userData.name || '',
            email: userData.email || '',
            subscriptionType: userData.isStaff ? 'admin' : 'user',
            createdAt: userData.dateJoined || '',
            lastLogin: userData.lastLogin || ''
        });

        // Registrar evento de inicio de sesión
        window.LogRocket.track('user_identified', {
            userId: userData.id,
            userType: userData.isStaff ? 'admin' : 'user',
            timestamp: new Date().toISOString()
        });
    } else {
        // Identificar como usuario anónimo
        const anonymousId = 'anonymous-' + Date.now();
        window.LogRocket.identify(anonymousId, {
            name: 'Anonymous User',
            type: 'anonymous',
            timestamp: new Date().toISOString()
        });
    }
}

// Función para registrar eventos personalizados
function logUserEvent(eventName, eventData) {
    if (window.LogRocket) {
        window.LogRocket.track(eventName, {
            ...eventData,
            timestamp: new Date().toISOString()
        });
    }
}

// Exportar las funciones
export { initializeLogRocketWithUser, logUserEvent };
