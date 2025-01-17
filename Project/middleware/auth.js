const isLogin = async (req, res, next) => {
    try {
        if (req.session.user_id) { }
        else {
            res.redirect('/login');
        }
        next();
    }
    catch (error) {
        console.log(error.message);
    }
};

const isLogout = async (req, res, next) => {
    try {
        if (req.session.user_id) {
            res.redirect('/profile');
        } next();
    } catch (error) {
        console.log(error.message);
    }
};
module.exports = {
    isLogin,
    isLogout
}