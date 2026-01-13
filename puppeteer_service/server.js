const express = require('express');
const puppeteer = require('puppeteer');
const bodyParser = require('body-parser');

const app = express();
const PORT = process.env.PORT || 3001; // Use port 3001 or specified by environment

app.use(bodyParser.json({ limit: '50mb' })); // Increased limit for large HTML content

app.post('/generate-pdf', async (req, res) => {
    const { htmlContent, options } = req.body;

    if (!htmlContent) {
        return res.status(400).send('HTML content is required.');
    }

    let browser;
    try {
        browser = await puppeteer.launch({
            headless: true, // Use 'new' for new headless mode, 'true' for old headless
            args: [
                '--no-sandbox', // Required for some environments
                '--disable-setuid-sandbox',
                '--font-render-hinting=none', // Ensure consistent font rendering
            ],
            // executablePath: '/usr/bin/google-chrome' // Specify path to Chrome/Chromium if not automatically found
        });
        const page = await browser.newPage();

        // Set content and wait for network idle to ensure all resources are loaded
        await page.setContent(htmlContent, { waitUntil: 'networkidle0' });

        // Apply PDF generation options based on the analysis
        // These options are crucial for matching R.book_03.pdf's layout
        const pdfOptions = {
            format: 'A4', // As inferred from analysis
            printBackground: true, // Essential for background colors/images
            margin: { // Based on the "Overall Layout & Structure" analysis
                top: '2.54cm',    // ~1 inch
                right: '1.9cm',   // ~0.75 inch
                bottom: '2.54cm', // ~1 inch
                left: '1.9cm',    // ~0.75 inch
            },
            // Emulate the @page CSS rules for headers/footers if needed,
            // or ensure they are part of the HTML content itself.
            // For now, rely on CSS @page rules for page numbers etc.
            ...options // Allow Python to override/add specific options
        };

        const pdfBuffer = await page.pdf(pdfOptions);

        res.set({
            'Content-Type': 'application/pdf',
            'Content-Length': pdfBuffer.length,
            'Content-Disposition': 'attachment; filename="report.pdf"',
        });
        res.send(pdfBuffer);

    } catch (error) {
        console.error('Error generating PDF:', error);
        res.status(500).send('Error generating PDF.');
    } finally {
        if (browser) {
            await browser.close();
        }
    }
});

app.listen(PORT, () => {
    console.log(`Puppeteer PDF service listening on port ${PORT}`);
});
