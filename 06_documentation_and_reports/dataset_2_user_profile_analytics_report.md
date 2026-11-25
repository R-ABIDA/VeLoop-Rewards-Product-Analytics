# VELoop Rewards – Dataset 2 User Profile Analytics Report

## 1. Dataset Overview

- **Dataset:** VELOOP Simulated User Behavior
- **Database Table:** `veloop.simulated_user_behavior`
- **Total Records:** 1,000
- **Unique User IDs:** 1,000
- **Analysis Type:** User Profile and Product Analytics

The dataset was analysed separately from Dataset 1, as instructed. The analysis covers account status, onboarding, verification, acquisition sources, demographics, geographic distribution, devices, registration trends, and referral-code attributes.

## 2. Account Status Analysis

| Account Status | Users | Percentage |
|---|---:|---:|
| Active | 602 | 60.20% |
| Inactive | 248 | 24.80% |
| Pending Verification | 84 | 8.40% |
| Suspended | 66 | 6.60% |
| **Total** | **1,000** | **100%** |

**Finding:** Active users represent 60.20% of the dataset. Inactive users account for 24.80%.

## 3. Onboarding Analysis

| Onboarding Status | Users | Percentage |
|---|---:|---:|
| Completed | 685 | 68.50% |
| Started | 162 | 16.20% |
| Not Started | 153 | 15.30% |
| **Total** | **1,000** | **100%** |

**Finding:** 68.50% of users completed onboarding, while 31.50% either started but did not complete it or did not start.

## 4. Verification Analysis

| Verification Status | Users | Percentage |
|---|---:|---:|
| Verified | 851 | 85.10% |
| Pending | 149 | 14.90% |
| **Total** | **1,000** | **100%** |

**Finding:** Most users have completed verification. A further 149 users have pending verification.

## 5. Acquisition Source Analysis

| Acquisition Source | Users | Percentage |
|---|---:|---:|
| Organic Search | 258 | 25.80% |
| Direct | 194 | 19.40% |
| Social Media | 162 | 16.20% |
| Referral | 154 | 15.40% |
| Other | 97 | 9.70% |
| WhatsApp | 75 | 7.50% |
| Telegram | 60 | 6.00% |
| **Total** | **1,000** | **100%** |

**Finding:** Organic Search is the largest acquisition source, contributing 25.80% of users.

## 6. Geographic Analysis

### Top 10 States

| State | Users | Percentage |
|---|---:|---:|
| Karnataka | 119 | 11.90% |
| West Bengal | 118 | 11.80% |
| Kerala | 92 | 9.20% |
| Haryana | 86 | 8.60% |
| Chhattisgarh | 73 | 7.30% |
| Maharashtra | 64 | 6.40% |
| Gujarat | 62 | 6.20% |
| Punjab | 52 | 5.20% |
| Uttar Pradesh | 46 | 4.60% |
| Madhya Pradesh | 45 | 4.50% |

**Finding:** Karnataka and West Bengal have the highest user counts among the ten states returned by the analysis.

### Top 10 Cities

| City | Users |
|---|---:|
| Raipur | 73 |
| Mangaluru | 46 |
| Kolkata | 44 |
| Faridabad | 43 |
| Gurugram | 43 |
| Durgapur | 42 |
| Mysuru | 39 |
| Kochi | 36 |
| Guwahati | 35 |
| Bengaluru | 34 |

**Finding:** Raipur has the highest user count among the top ten cities.

## 7. Age Group Analysis

| Age Group | Users | Percentage |
|---|---:|---:|
| 18–24 | 303 | 30.30% |
| 25–34 | 463 | 46.30% |
| 35–44 | 234 | 23.40% |
| **Total** | **1,000** | **100%** |

**Finding:** The 25–34 age group represents the largest segment, with 46.30% of users.

## 8. Gender Analysis

| Gender | Users | Percentage |
|---|---:|---:|
| Female | 336 | 33.60% |
| Male | 343 | 34.30% |
| Prefer not to say | 321 | 32.10% |
| **Total** | **1,000** | **100%** |

## 9. Primary Device Analysis

| Device | Users | Percentage |
|---|---:|---:|
| Android | 675 | 67.50% |
| Windows | 148 | 14.80% |
| iOS | 125 | 12.50% |
| macOS | 52 | 5.20% |
| **Total** | **1,000** | **100%** |

**Finding:** Android is the most frequently reported primary device.

## 10. Platform Analysis

| Platform | Users | Percentage |
|---|---:|---:|
| Web | 1,000 | 100% |

**Finding:** All records in this dataset identify Web as the platform.

## 11. Referral Source Detail Analysis

| Referral Source Detail | Users | Percentage |
|---|---:|---:|
| Friend/Family | 154 | 15.40% |
| Not specified | 846 | 84.60% |
| **Total** | **1,000** | **100%** |

**Finding:** Referral-source detail is not specified for 84.60% of users.

## 12. Monthly Registration Analysis

| Month | Registrations |
|---|---:|
| April 2026 | 186 |
| May 2026 | 167 |
| June 2026 | 182 |
| July 2026 | 182 |
| August 2026 | 177 |
| September 2026 | 106 |
| **Total** | **1,000** |

**Finding:** April has the highest registration count in the supplied results. September has the lowest count; confirm whether September represents a complete month before interpreting the difference.

## 13. Account Status by State

The analysis grouped users by state and account status to identify the distribution of Active, Inactive, Suspended, and Pending Verification accounts across locations.

The complete SQL output contains the state-wise breakdown.

## 14. Onboarding by Acquisition Source

The analysis grouped onboarding status by acquisition channel.

It helps compare Completed