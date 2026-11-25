# VELoop Rewards – Dataset 1 User Analytics Report

## 1. Dataset Overview

- **Database:** `veloop_rewards`
- **Schema:** `veloop`
- **Table:** `users`
- **Total Records:** 1,000
- **Unique User IDs:** 1,000
- **Analysis Type:** User Profile and Engagement Attribute Analysis

This analysis uses the first original VELoop Rewards dataset. It is kept separate from Dataset 2.

## 2. Account Status Analysis

| Account Status | Users | Percentage |
|---|---:|---:|
| Active | 568 | 56.80% |
| Inactive | 283 | 28.30% |
| Suspended | 77 | 7.70% |
| Pending Verification | 72 | 7.20% |
| **Total** | **1,000** | **100%** |

**Finding:** Active users represent 56.80% of the dataset.

## 3. Onboarding Status Analysis

| Onboarding Status | Users | Percentage |
|---|---:|---:|
| Completed | 722 | 72.20% |
| Started | 146 | 14.60% |
| Not Started | 132 | 13.20% |
| **Total** | **1,000** | **100%** |

**Finding:** 72.20% of users completed onboarding. The remaining 27.80% have not completed it.

## 4. Acquisition Source Analysis

| Acquisition Source | Users | Percentage |
|---|---:|---:|
| Organic Search | 244 | 24.40% |
| Direct | 217 | 21.70% |
| Social Media | 160 | 16.00% |
| Referral | 119 | 11.90% |
| WhatsApp | 103 | 10.30% |
| Other | 102 | 10.20% |
| Telegram | 55 | 5.50% |
| **Total** | **1,000** | **100%** |

**Finding:** Organic Search is the largest acquisition source.

## 5. Geographic Analysis

### Top 10 States

| State | Users | Percentage |
|---|---:|---:|
| Kerala | 129 | 12.90% |
| Uttar Pradesh | 122 | 12.20% |
| Bihar | 92 | 9.20% |
| Odisha | 83 | 8.30% |
| Maharashtra | 67 | 6.70% |
| Telangana | 63 | 6.30% |
| Karnataka | 63 | 6.30% |
| West Bengal | 56 | 5.60% |
| Gujarat | 49 | 4.90% |
| Punjab | 48 | 4.80% |

**Finding:** Kerala has the highest number of users in the dataset.

### Top 10 Cities

| City | Users | Percentage |
|---|---:|---:|
| Kochi | 129 | 12.90% |
| Bhubaneswar | 83 | 8.30% |
| Hyderabad | 63 | 6.30% |
| Gaya | 49 | 4.90% |
| Ludhiana | 48 | 4.80% |
| Noida | 44 | 4.40% |
| Patna | 43 | 4.30% |
| Kanpur | 40 | 4.00% |
| Lucknow | 38 | 3.80% |
| New Delhi | 38 | 3.80% |

## 6. Age Group Analysis

| Age Group | Users | Percentage |
|---|---:|---:|
| 18–24 | 354 | 35.40% |
| 25–34 | 448 | 44.80% |
| 35–44 | 198 | 19.80% |
| **Total** | **1,000** | **100%** |

**Finding:** The 25–34 age group is the largest user segment.

## 7. Gender Analysis

| Gender | Users | Percentage |
|---|---:|---:|
| Male | 343 | 34.30% |
| Female | 331 | 33.10% |
| Prefer not to say | 326 | 32.60% |
| **Total** | **1,000** | **100%** |

## 8. Platform Analysis

| Platform | Users | Percentage |
|---|---:|---:|
| Web | 1,000 | 100% |

**Finding:** All records identify Web as the platform.

## 9. Primary Device Analysis

| Device | Users | Percentage |
|---|---:|---:|
| Android | 659 | 65.90% |
| Windows | 155 | 15.50% |
| iOS | 140 | 14.00% |
| macOS | 46 | 4.60% |
| **Total** | **1,000** | **100%** |

**Finding:** Android is the most common primary device.

## 10. Email Verification Analysis

| Verification Status | Users | Percentage |
|---|---:|---:|
| Verified | 855 | 85.50% |
| Pending | 145 | 14.50% |
| **Total** | **1,000** | **100%** |

## 11. Consent Analysis

| Consent Status | Users | Percentage |
|---|---:|---:|
| Accepted | 923 | 92.30% |
| Pending | 77 | 7.70% |
| **Total** | **1,000** | **100%** |

## 12. Marketing Opt-in Analysis

| Marketing Opt-in | Users | Percentage |
|---|---:|---:|
| No | 558 | 55.80% |
| Yes | 442 | 44.20% |
| **Total** | **1,000** | **100%** |

## 13. XP Balance Analysis

| Metric | Value |
|---|---:|
| Total Users | 1,000 |
| Average XP Balance | 231.89 |
| Minimum XP Balance | 5 |
| Maximum XP Balance | 1,156 |
| Total XP Balance | 231,889 |

**Finding:** The average XP balance across users is 231.89.

## 14. User Activity Analysis

### Seven-Day Activity

| Activity | Users | Percentage |
|---|---:|---:|
| Active | 78 | 7.80% |
| Inactive | 922 | 92.20% |

### Thirty-Day Activity

| Activity | Users | Percentage |
|---|---:|---:|
| Active | 325 | 32.50% |
| Inactive | 675 | 67.50% |

**Finding:** The recorded seven-day activity flag is lower than the thirty-day activity flag.

## 15. Monthly Registration Analysis

| Month | Registrations |
|---|---:|
| April 2026 | 174 |
| May 2026 | 179 |
| June 2026 | 166 |
| July 2026 | 198 |
| August 2026 | 192 |
| September 2026 | 91 |
| **Total** | **1,000** |

**Finding:** July has the highest registration count in the supplied results. September has the lowest count; confirm whether September covers a complete month before interpreting the trend.

## 16. Account Status by State

The analysis groups users by state and account status to understand the geographic distribution of Active, Inactive, Suspended, and Pending Verification accounts.

The complete state-wise SQL output should be retained as supporting evidence.

## 17. Onboarding by Acquisition Source

The analysis groups onboarding status by acquisition source.

It helps compare Completed, Started, and Not Started users across Direct, Organic Search, Other, Referral, Social Media, Telegram, and WhatsApp.

## 18. Recommendations

1. Review users who have not completed onboarding.
2. Investigate the large number of users marked inactive in the seven-day activity flag.
3. Monitor verification-pending accounts.
4. Review acquisition-channel performance.
5. Examine device distribution when planning user experience improvements.
6. Monitor registration trends and validate the September reporting period.
7. Review consent and marketing opt-in records when planning communication campaigns.

## 19. Conclusion

The Dataset 1 analysis provides insights into user accounts, onboarding, acquisition, demographics, geographic distribution, devices, verification, consent, XP balances, activity flags, and registration trends.

The results show that Organic Search is the largest acquisition source, the 25–34 age group is the largest demographic segment, and Android is the most common primary device.

The findings can support user segmentation, onboarding improvement, acquisition monitoring, and product analytics reporting.

**Scope limitation:** This report uses the supplied Dataset 1 only. User activity flags and lifetime session attributes are profile-level fields; they do not replace detailed event-level session, wallet, withdrawal, task, or feature-event records.

**Data handling:** Dataset 1 remains separate from Dataset 2. The original supplied data has not been merged or modified for this report.