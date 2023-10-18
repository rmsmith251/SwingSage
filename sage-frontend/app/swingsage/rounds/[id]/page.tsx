import { SwingSageFooter } from "@/app/common";

export default function RoundPage({ params }: { params: { id: string }}) {
    return (
        <main className="flex min-h-screen flex-col items-center justify-between p-24">
            <div>
                Round ID: {params.id}
                <SwingSageFooter />
            </div>
        </main>
    )
}