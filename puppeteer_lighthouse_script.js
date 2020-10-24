'use strict';

/**
 * Script for running Lighthouse on an authenticated page using puppeteer.
 */

const lighthouse = require('lighthouse');
const puppeteer = require('puppeteer');
require('dotenv').config();
const fs = require('fs');
var path = require("path");

// This port will be used by Lighthouse later. The specific port is arbitrary.
const PORT = 8041;

/**
 * @param {import('puppeteer').Browser} browser
 * @param {string} origin
 */
async function login(browser, origin) {
  const page = await browser.newPage();
  await page.goto(origin);
  await page.waitForSelector('input[type="text"]', {visible: true});

  // Fill in and submit login form.
  const userName = await page.$('input[type="text"]');
  await userName.type(process.env.TEST_USERNAME);
  const passwordInput = await page.$('input[type="password"]');
  await passwordInput.type(process.env.TEST_PASSWORD);
  await Promise.all([
    page.$eval('form', form => form.submit()),
    page.waitForNavigation(),
  ]).catch(function () {
     console.log("Promise Rejected");
});

  await page.close();
}

/**
 * @param {puppeteer.Browser} browser
 * @param {string} origin
 */
async function logout(browser, origin) {
  const page = await browser.newPage();
  await page.goto(`${origin}/logout`);
  await page.close();
}

async function main() {

  // console.log('Starting...')

  // Direct Puppeteer to open Chromium/Chrome with a specific debugging port.
  const browser = await puppeteer.launch({
    args: [`--remote-debugging-port=${PORT}`],
    // Optional, if you want to see the tests in action.
    headless: true,
    slowMo: 50,
  });

  // Setup the browser session to be logged into our site.
  const SERVER_URL = process.env.TEST_SERVER_URL;

  // The local server is running on port 10632.

  const auth_urls = [
    '/accounts/login',
  ]

  const selfservice_urls = [
    '','/view-announcements','/selfservice/me','selfservice/payslip-history','/selfservice/pension-history', '/selfservice/my/subordinates',
    '/selfservice/leave/plans','/leave/new-plan','/selfservice/leave/history','/selfservice/leave/apply','/selfservice/loan-history',
    '/selfservice/loans/apply','/selfservice/appraisals/history','/selfservice/claim-history','/selfservice/claims/apply',
    '/selfservice/medical-claim-history','/selfservice/medical-claims/apply','/selfservice/overtime/overtime-history',
    '/selfservice/overtime/add','/selfservice/overtime/overtime-history','/selfservice/overtime/add','/selfservice/salary-advance-history',
    '/selfservice/salary-advance-add','/selfservice/training/','/selfservice/training-requests/all','/selfservice/request-training',
    '/selfservice/manager/evaluations','/appraisals/evaluations/create','/selfservice/supervise/appraisals',
    ]

  const employees_urls = [
    '/employees','/employees/employee-types','/employees/employee-types/new','employees/leave-plans/all','/employees/leaves',
    '/employees/attendance/entry_list', '/employees/attendance/entry/add', '/employees/attendance/entry/upload', '/employees/termination', 
    '/employees/termination/create','/employees/termination/exitreason', '/employees/promotion/single/new', '/employees/promotion/group/new',
    '/employees/incident','/employees/placements/new/','/employees/employee-reports','/employees/import-batches','/employees/import-batches/upload',
    '/employees/leaves/add', '/employees/leaves/types', '/employees/leaves/types/add','/employees/leaves/types','/employees/leaves/types/add',
    '/employees/leaves/policy','employees/leaves/policy/add', '/employees/absence','/employees/termination/exitreason/create', '/employees/promotion/all',
    '/employees/incident/add', '/employees/placements/all', '/employees/metric/female2male-2',
  
  ]

  const payroll_urls = [
    '/payroll/dashboard', '/payroll/batches', '/payroll/process', '/payroll/pay-types', '/payroll/pay-items', '/payroll/pay-items/add',
    '/payroll/pay-templates', '/payroll/pay-templates/add', '/payroll/pay-templates/assign-to-employees', '/payroll/pay-options', '/payroll/pay-options/add',
    '/payroll/claim/claim-types', '/payroll/claims', '/payroll/claim/client', '/payroll/medical-claims', '/payroll/medical-claims/records/upload',
    '/payroll/loans/add','/payroll/loans/loan-types', '/payroll/loans/loan-types/add', '/payroll/standingorder/categories', '/payroll/standingorder',
    '/payroll/overtime','/payroll/overtime/add', '/payroll/overtime/records/upload', '/payroll/spot-bonus/category', '/payroll/spot-bonus/category/add',
    '/payroll/spot-bonus','/payroll/spot-bonus/apply', '/payroll/spot-deduction/category', '/payroll/spot-deduction/category/add', '/payroll/spot-deduction',
    '/payroll/spot-deduction/apply', '/payroll/advance', '/payroll/advance/apply', '/payroll/401k', '/payroll/401k/create','/payroll/garnishment',
    '/payroll/garnishment/apply', '/payroll/payroll-reports', '/payroll/pay-types/add', '/payroll/claim/claim-types/add', '/payroll/claims/add', 
    '/payroll/claim/client/sites','/payroll/claim/client/sites/add','/payroll/claim/client/add', '/payroll/medical-claims/add','/payroll/loans', 
    '/payroll/standingorder/categories/add', '/payroll/standingorder/subscriptions','/payroll/standingorder/subscriptions/add-individual',
  ]

  const careers_urls = [
    '/careers/dashboard', '/careers/training-request-report', '/careers/employee-training-report', '/careers/course-types', '/careers/course-types/add',
    '/careers/roles', '/careers/role/add', '/careers/skill-levels','/careers/skill-levels/add','/careers/skills','/careers/skills/add', '/careers/course/report'
  ]

  const company_urls = [
    'company/dashboard','/company/announcements','company/announcements/add','/company/holidays','/company/holidays/add','/company/dynamicgroups',
    '/company/gradelevels','/company/gradelevels/records/upload','/company/unit/types','/company/unit/types/add','/company/unit','/company/units/records/upload',
    '/company/position','/company/position/add','/company/position/records/upload','/company/locations','/company/locations/records/upload','/company/banks',
    '/company/banks/add','/company/corporate-accounts','/company/pensioncustodian','/company/pensioncustodian/add','/company/pensionadministrator',
    '/company/pensionadministrator/add','/company/insurers','/company/insurers/add','/company/dynamicgroups/add', '/company/gradelevels/add',
    '/company/units/add','/company/locations/add','/company/corporate-accounts/add'
  ]

  const appraisals_url = [
    '/appraisals/dashboard/', '/appraisals/evaluations', '/appraisals/evaluations/create', '/appraisals/perspectives', '/appraisals/perspectives/create',
    '/appraisals/appraisal-reasons','/appraisals/appraisal-reasons/new', '/appraisals/strategies', '/appraisals/strategies/create', '/appraisals/rating',
    '/appraisals/rating/add'
  ]

  const medical_urls = [
    '/medical/dashboard','/medical/hmo','/medical/hmos/add','/medical/providers/all','/medical/providers/add','/medical/providers/records/upload',
    '/medical/coverages/all','/medical/coverage/add','/medical/reports/claims','/medical/reports/employee-plan-enrolment','/medical/change-employee/plans'
  ]

  const operations_urls = [
    '/operation','/operation/crude-events','/operation/request-events', '/operation/users','/operation/permissions','/operation/groups','/operation/groups/new',
    '/operation/login-events',
  ]

  const timesheet_urls = [
    '/projects','/projects/list','/projects/add','/projects/entries','/projects/entry/add','/projects/entries/upload','/projects/list/project-type',
    '/projects/add/project-type','/projects/list/businesses','/projects/add/business','/projects/list/activities','/projects/add/activity'
  ]

  // const urls = [
  //   ...auth_urls, ...selfservice_urls, ...employees_urls, ...payroll_urls, ...careers_urls, ...company_urls,
  //   ...appraisals_url, ...medical_urls, ...operations_urls, ...timesheet_urls,
  // ]

  const urls = [
    '/','/employees/upload-records/'
  ]

  // generate report for authenticated links
  await login(browser, SERVER_URL);

  for (const url of urls){
    
    // Direct Lighthouse to use the same port.
    let link = SERVER_URL+url+'/';
    let result = await lighthouse(link, {port: PORT, disableStorageReset: true}).catch(function () {
       console.log("Lighthouse error at " + link);
    });

    // Output the result to file created
    if (result) {
      let data = JSON.stringify(result.lhr, null, 2);
      let filename = `audit_report_for${url.replace(/\//g, '_')}.json`

      const directory = 'Audit_Reports'
      if (!fs.existsSync(directory)) {
        fs.mkdirSync(directory);
        console.log('Directory created');
    }

      fs.writeFile(directory/filename, data, (err) => {
        if (err) {
            throw err;
        }
      });
      console.log(`${url} -> audit successful`);
       const path = `/home/runner/work/Duty-Register/Duty-Register/Audit_Reports/${filename}`
      fs.access(path, fs.F_OK, (err) => {
        if (err) {
          // console.log(__dirname)
          console.log('file doesnt exist');
          console.error(err)
          return
        }
        console.log(`${path} -> file exits`)
        //file exists
      })

    }else{
      console.log(`${url} -> audit failed`);
    }
    
  }

  // All auditing completed
  console.log('All auditing completed');

  // Direct Puppeteer to close the browser as we're done with it.
  await browser.close();
}

if (require.main === module) {
  main();
  // console.log(process.env.TEST_USERNAME, process.env.TEST_PASSWORD)
} else {
  module.exports = {
    login,
    logout,
  };
}