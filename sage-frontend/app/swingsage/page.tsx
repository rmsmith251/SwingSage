import { SwingSageFooter} from "../common"
// function getLocation(): Promise<GeolocationPosition> {
//     return new Promise((resolve, reject) => {
//         if (navigator.geolocation) {
//             navigator.geolocation.getCurrentPosition(
//                 position => resolve(position),
//                 error => reject(error)
//             );
//         } else {
//             reject(new Error("Geolocation is not supported by this browser."));
//         }
//     });
// }
export default function SwingSage() {
    return (
        <main className="flex min-h-screen flex-col items-center justify-between p-24">
            <SwingSageFooter />
            </main>
    )
}