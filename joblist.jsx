// import React from 'react';
// import { useState } from 'react';
// import jobsData from '../Joblist/indeed1.json'; // Adjust path as needed
// import Navbar from '../Navbar/navbar';
// function JobList({jobs}) {
  


//   return (
//     <div>
//       <Navbar/>

//       <h1>Job Listings</h1>


//       {/* search bar */}
//       <form class="max-w-md mx-auto">
//         <label for="default-search" class="mb-2 text-sm font-medium text-gray-900 sr-only dark:text-white">Search</label>
//         <div class="relative">
//           <div class="absolute inset-y-0 start-0 flex items-center ps-3 pointer-events-none">
//             <svg class="w-4 h-4 text-gray-500 dark:text-gray-400" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 20 20">
//               <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m19 19-4-4m0-7A7 7 0 1 1 1 8a7 7 0 0 1 14 0Z" />
//             </svg>
//           </div>
//           <input type="search" id="default-search" class="block w-full p-4 ps-10 text-sm text-gray-900 border border-gray-300 rounded-lg bg-gray-50 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="Search Mockups, Logos..." required />
//           <button type="submit" class="text-white absolute end-2.5 bottom-2.5 bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-4 py-2 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">Search</button>
//         </div>
//       </form>


//       <ul>

//         {jobsData.map((job, index) => (
//           <li key={index} className="mb-6">
//             <h2 className="text-xl font-bold">
//               <a href={job.JobTitle_link} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline">
//                 {job.JobTitle}
//               </a>
//             </h2>

//             {/* Flex container for company and location */}
//             <div className="flex gap-2 mb-4 justify-start">
//               {/* Company box */}
//               <p className="border-2 border-gray-300 p-2 rounded-md bg-gray-10 w-50 text-center">
//                 <strong>Company:</strong> {job.Company}
//               </p>

//               {/* Location box */}
//               <p className="border-2 border-gray-300 p-2 rounded-md bg-gray-10  w-40 text-center">
//                 <strong>Location:</strong> {job.location}
//               </p>
//             </div>

//             {/* Requirements */}
//             <p className="text-gray-700"><strong>Requirements:</strong> {job.Requirements}</p>
//           </li>


//         ))}
//       </ul>
//     </div>
//   );
// }

// export default JobList;


import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Navbar from '../Navbar/navbar';

function JobList() {
  const [jobs, setJobs] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    // Fetch jobs from the backend API
    axios.get('http://localhost:5000/api/jobs')
      .then(response => {
        setJobs(response.data);
      })
      .catch(error => {
        console.error('Error fetching jobs:', error);
      });
  }, []);

  const handleSearch = (e) => {
    e.preventDefault();
    const filteredJobs = jobs.filter(job => job.JobTitle.toLowerCase().includes(searchQuery.toLowerCase()));
    setJobs(filteredJobs);
  };

  return (
    <div>
      <Navbar />
      <h1>Job Listings</h1>

      {/* Search bar */}
      <form className="max-w-md mx-auto" onSubmit={handleSearch}>
        <label htmlFor="default-search" className="mb-2 text-sm font-medium text-gray-900 sr-only dark:text-white">Search</label>
        <div className="relative">
          <div className="absolute inset-y-0 start-0 flex items-center ps-3 pointer-events-none">
            <svg className="w-4 h-4 text-gray-500 dark:text-gray-400" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 20 20">
              <path stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="m19 19-4-4m0-7A7 7 0 1 1 1 8a7 7 0 0 1 14 0Z" />
            </svg>
          </div>
          <input 
            type="search" 
            id="default-search" 
            className="block w-full p-4 ps-10 text-sm text-gray-900 border border-gray-300 rounded-lg bg-gray-50 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
            placeholder="Search Jobs..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            required 
          />
          <button type="submit" className="text-white absolute end-2.5 bottom-2.5 bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-4 py-2 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">Search</button>
        </div>
      </form>

      <ul>
        {jobs.map((job, index) => (
          <li key={index} className="mb-6">
            <h2 className="text-xl font-bold">
              <a href={job.JobTitle_link} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline">
                {job.JobTitle}
              </a>
            </h2>
            <div className="flex gap-2 mb-4 justify-start">
              <p className="border-2 border-gray-300 p-2 rounded-md bg-gray-10 w-50 text-center">
                <strong>Company:</strong> {job.Company}
              </p>
              <p className="border-2 border-gray-300 p-2 rounded-md bg-gray-10 w-40 text-center">
                <strong>Location:</strong> {job.location}
              </p>
            </div>
            <p className="text-gray-700"><strong>required:</strong> {job.SkillsRequired}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default JobList;

