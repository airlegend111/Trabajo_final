UPDATE users_userprofile 
SET role = 'ADMIN', full_name = 'Carlos Andres Baena Moncada'
WHERE user_id = (SELECT id FROM auth_user WHERE username = 'Pupu');
