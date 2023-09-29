import React from 'react';

const Footer = () => {
  return (
    <footer className="footer">
		<div className="footer-contact">
            <div className="footer-contact-info">
            </div>
            <ul className="footer-contact-media">
                <li className="footer-contact-media-element"><a className="telegram" href=""><i class="fab fa-telegram"></i></a></li>
                <li className="footer-contact-media-element"><a className="instagram" href=""><i class="fab fa-instagram"></i></a></li>
                <li className="footer-contact-media-element"><a className="vk" href=""><i class="fab fa-vk"></i></a></li>
            </ul>
        </div>
        <div className='footer-credentials'>&copy; Taipex. All rights reserved.</div>
    </footer>
  );
};

export default Footer;