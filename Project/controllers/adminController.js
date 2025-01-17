// 1st get admin model
const User = require('../models/userModel');

// for hiding password
const bcrypt = require('bcrypt');



const loadlogin = async (req, res) => {
    try {
        res.render('login');
    } catch (error) {
        console.log(error.message);
    }
}


const verifyLogin = async (req, res) => {
    try {
        const email = req.body.email;
        const password = req.body.password;
        const userData = await User.findOne({ email: email });
        if (userData) {
            const matchPassword = await bcrypt.compare(password, userData.password);

            if (matchPassword) {
                if (userData.is_admin === 0) {
                    res.render('login', { message: "Email or password is incorrect" });
                } else {
                    req.session.user_id = userData._id;
                    res.redirect('/admin/home');
                }
            } else {
                res.render('login', { message: "Email or password is incorrect" });
            }
        } else {
            res.render('login', { message: "Email or password is incorrect" });
        }
    } catch (error) {
        console.log(error.message);
    }
}

const loadDashboard = async (req, res) => {
    try {
        const userData = await User.findById({ _id: req.session.user_id })
        res.render('home', { users: userData });
    } catch (error) {
        console.log(error.message);
    }
}

const loadprofile = async (req, res) => {
    try {
        const userData = await User.findById({ _id: req.session.user_id })
        res.render('profile', { user_detail: userData });
    } catch (error) {
        console.log(error.message);
    }
}

const logout = async (req, res) => {
    try {
        req.session.destroy();
        res.redirect('/admin');
    } catch (error) {
        console.log(error.message);
    }
}

const adminDashboard = async (req, res) => {
    try {
        const userData = await User.find({ is_admin: 0 });
        res.render('dashboard', { users: userData });

    } catch (error) {
        console.log(error.message);
    }
}

module.exports = {
    loadlogin,
    verifyLogin,
    loadDashboard,
    logout,
    adminDashboard
}
