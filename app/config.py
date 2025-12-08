import os

require('dotenv').config();

module.exports = {
  PORT: process.env.PORT || 8080,
  BLOG_ID: process.env.BLOG_ID,
  API_KEY: process.env.API_KEY
};
